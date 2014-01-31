/*
   Copyright (C) 2014  Statoil ASA, Norway.

   The file 'enkf_plot_gendata.c' is part of ERT - Ensemble based Reservoir Tool.

   ERT is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   ERT is distributed in the hope that it will be useful, but WITHOUT ANY
   WARRANTY; without even the implied warranty of MERCHANTABILITY or
   FITNESS FOR A PARTICULAR PURPOSE.

   See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
   for more details.
*/


#include <time.h>
#include <stdbool.h>

#include <ert/util/double_vector.h>
#include <ert/util/vector.h>
#include <ert/util/thread_pool.h>
#include <ert/util/type_macros.h>

#include <ert/enkf/enkf_fs.h>
#include <ert/enkf/block_obs.h>
#include <ert/enkf/obs_vector.h>
#include <ert/enkf/enkf_node.h>

#define ENKF_PLOT_GENDATA_TYPE_ID 6676266669

struct enkf_plot_genvector_struct {
  UTIL_TYPE_ID_DECLARATION;
  int iens;
  double_vector_type * data;
  const obs_vector_type * obs_vector;
};

UTIL_IS_INSTANCE_FUNCTION( enkf_plot_gendata , ENKF_PLOT_GENDATA_TYPE_ID )

enkf_plot_genector_type * enkf_plot_genvector_alloc( const obs_vector_type * obs_vector , int iens){
    enkf_plot_genvector_type * vector = util_malloc(sizeof * vector);
    UTIL_TYPE_ID_INIT( vector , ENKF_PLOT_BLOCKVECTOR_TYPE_ID );
    vector->obs_vector = obs_vector;
    vector->data = double_vector_alloc(0,0);
    vector->iens = iens;
    return vector;
}

void enkf_plot_genvector_free( enkf_plot_genvector_type * vector ){
    double_vector_free(vector->data);
    free(vector);
}

int enkf_plot_genvector_get_size( const enkf_plot_genvector_type * vector ){
    return double_vector_size( vector->data );
}

void enkf_plot_genvector_reset( enkf_plot_genvector_type * vector )
{

}

void * enkf_plot_genvector_load__( void * arg ){}

double enkf_plot_genvector_iget( const enkf_plot_genvector_type * vector , int index){}