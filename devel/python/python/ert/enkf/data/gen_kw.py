#  Copyright (C) 2012  Statoil ASA, Norway. 
#   
#  The file 'gen_kw.py' is part of ERT - Ensemble based Reservoir Tool.
#   
#  ERT is free software: you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation, either version 3 of the License, or 
#  (at your option) any later version. 
#   
#  ERT is distributed in the hope that it will be useful, but WITHOUT ANY 
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#  FITNESS FOR A PARTICULAR PURPOSE.   
#   
#  See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html> 
#  for more details.
from ert.cwrap import BaseCClass, CWrapper, CFILE
from ert.enkf import ENKF_LIB
from ert.enkf.data import GenKwConfig


class GenKw(BaseCClass):
    def __init__(self, gen_kw_config):
        """
         @type gen_kw_config: GenKwConfig
        """
        c_ptr = GenKw.cNamespace().alloc(gen_kw_config)
        super(GenKw, self).__init__(c_ptr)

    def exportParameters(self, file_name):
        """ @type: str """
        py_fileH = open(file_name , "w")
        cfile  = CFILE( py_fileH )
        GenKw.cNamespace().export_parameters(self, cfile)
        py_fileH.close()

    def exportTemplate(self, file_name):
        """ @type: str """
        GenKw.cNamespace().export_template(self, file_name)

    def free(self):
        GenKw.cNamespace().free(self)


    def __getitem__(self, key):
        """
        @type key: int or str
        @rtype: float
        """
        if isinstance(key, str):
            return GenKw.cNamespace().data_get(self, key, False)
        elif isinstance(key, int):
            return GenKw.cNamespace().data_iget(self, key, False)


    def __setitem__(self, key, value):
        """
        @type key: int or str
        @type value: float
        """
        if isinstance(key, str):
            return GenKw.cNamespace().data_set(self, key, value)
        elif isinstance(key, int):
            return GenKw.cNamespace().data_iset(self, key, value)





    ##################################################################

cwrapper = CWrapper(ENKF_LIB)
cwrapper.registerObjectType("gen_kw", GenKw)

GenKw.cNamespace().free = cwrapper.prototype("void gen_kw_free(gen_kw_config)")
GenKw.cNamespace().alloc = cwrapper.prototype("c_void_p gen_kw_alloc(gen_kw_config)")
GenKw.cNamespace().export_parameters = cwrapper.prototype("void gen_kw_write_export_file(gen_kw , FILE)")
GenKw.cNamespace().export_template = cwrapper.prototype("void gen_kw_ecl_write_template(gen_kw , char* )")
GenKw.cNamespace().data_iget = cwrapper.prototype("double gen_kw_data_iget(gen_kw, int, bool)")
GenKw.cNamespace().data_iset = cwrapper.prototype("void gen_kw_data_iset(gen_kw, int, double)")
GenKw.cNamespace().data_get = cwrapper.prototype("double gen_kw_data_get(gen_kw, char*, bool)")
GenKw.cNamespace().data_set = cwrapper.prototype("void gen_kw_data_set(gen_kw, char*, double)")