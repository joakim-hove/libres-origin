from PyQt4.QtCore import Qt, QSize, pyqtSignal
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QFrame, QToolButton, QAction
from ert_gui.models.connectors.init import CaseList
from ert_gui.models.connectors.run import SimulationModeModel
from ert_gui.pages.run_dialog import RunDialog
from ert_gui.simulation import EnsembleExperimentPanel, EnsembleSmootherPanel, IteratedEnsembleSmootherPanel
from ert_gui.simulation.simulation_config_panel import SimulationConfigPanel
from ert_gui.widgets import util

from ert_gui.widgets.combo_choice import ComboChoice
from ert_gui.widgets.helped_widget import HelpedWidget


class SimulationPanel(QWidget):

    show_advanced_options = pyqtSignal(bool)

    def __init__(self):
        QWidget.__init__(self)

        layout = QVBoxLayout()

        simulation_mode_layout = QHBoxLayout()
        simulation_mode_layout.addSpacing(10)
        simulation_mode_model = SimulationModeModel()
        simulation_mode_model.observable().attach(SimulationModeModel.CURRENT_CHOICE_CHANGED_EVENT, self.toggleSimulationMode)
        simulation_mode_combo = ComboChoice(simulation_mode_model, "Simulation mode", "run/simulation_mode")
        simulation_mode_layout.addWidget(QLabel(simulation_mode_combo.getLabel()), 0, Qt.AlignVCenter)
        simulation_mode_layout.addWidget(simulation_mode_combo, 0, Qt.AlignVCenter)

        # simulation_mode_layout.addStretch()
        simulation_mode_layout.addSpacing(20)

        self.run_button = QToolButton()
        self.run_button.setIconSize(QSize(32, 32))
        self.run_button.setText("Start Simulation")
        self.run_button.setIcon(util.resourceIcon("ide/gear_in_play"))
        self.run_button.clicked.connect(self.runSimulation)
        self.run_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        HelpedWidget.addHelpToWidget(self.run_button, "run/start_simulation")

        simulation_mode_layout.addWidget(self.run_button)
        simulation_mode_layout.addStretch(1)

        layout.addSpacing(5)
        layout.addLayout(simulation_mode_layout)
        layout.addSpacing(10)

        self.simulation_stack = QStackedWidget()
        self.simulation_stack.setLineWidth(1)
        self.simulation_stack.setFrameStyle(QFrame.StyledPanel)

        layout.addWidget(self.simulation_stack)

        self.simulation_widgets = {}

        self.addSimulationConfigPanel(EnsembleExperimentPanel())
        self.addSimulationConfigPanel(EnsembleSmootherPanel())
        self.addSimulationConfigPanel(IteratedEnsembleSmootherPanel())

        self.setLayout(layout)


    def addSimulationConfigPanel(self, panel):
        assert isinstance(panel, SimulationConfigPanel)

        panel.toggleAdvancedOptions(False)
        self.simulation_stack.addWidget(panel)
        self.simulation_widgets[panel.getSimulationModel()] = panel

        panel.simulationConfigurationChanged.connect(self.validationStatusChanged)


    def getActions(self):
        """ @rtype: list of QAction """
        advanced_toggle_action = QAction("Show Advanced Options", self)
        advanced_toggle_action.setObjectName("AdvancedSimulationOptions")
        advanced_toggle_action.setCheckable(True)
        advanced_toggle_action.setChecked(False)
        advanced_toggle_action.toggled.connect(self.toggleAdvanced)

        return [advanced_toggle_action]


    def toggleAdvanced(self, show_advanced):
        self.show_advanced_options.emit(show_advanced)
        for panel in self.simulation_widgets.values():
            panel.toggleAdvancedOptions(show_advanced)


    def getCurrentSimulationMode(self):
        return SimulationModeModel().getCurrentChoice()


    def runSimulation(self):
        run_model = self.getCurrentSimulationMode()

        dialog = RunDialog(run_model)
        dialog.startSimulation()
        dialog.exec_()

        CaseList().externalModificationNotification() # simulations may have added new cases.


    def toggleSimulationMode(self):
        widget = self.simulation_widgets[self.getCurrentSimulationMode()]
        self.simulation_stack.setCurrentWidget(widget)
        self.validationStatusChanged()


    def validationStatusChanged(self):
        widget = self.simulation_widgets[self.getCurrentSimulationMode()]
        self.run_button.setEnabled(widget.isConfigurationValid())




