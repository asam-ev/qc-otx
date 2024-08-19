# Checker bundle: otxBundle

* Build version:  0.1.0
* Description:    OTX checker bundle

## Parameters

* InputFile: 

## Checkers

### core_otx

* Description: Check if core properties of input file are properly set
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_001.document_name_matches_filename
  * asam.net:otx:1.0.0:core.chk_002.document_name_package_uniqueness
  * asam.net:otx:1.0.0:core.chk_003.no_dead_import_links
  * asam.net:otx:1.0.0:core.chk_004.no_unused_imports
  * asam.net:otx:1.0.0:core.chk_005.no_use_of_undefined_import_prefixes
  * asam.net:otx:1.0.0:core.chk_006.match_of_imported_document_data_model_version
  * asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists
  * asam.net:otx:1.0.0:core.chk_008.public_main_procedure
  * asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization
  * asam.net:otx:1.0.0:core.chk_010.unique_node_names

### data_type_otx

* Description: Check if data_type properties of input file are properly set
* Addressed rules:
  * asam.net:otx:1.0.0:data_type.chk_001.accessing_structure_elements
  * asam.net:otx:1.0.0:data_type.chk_008.correct_target_for_structure_element

### zip_file_otx

* Description: Check if zip_file properties of input file are properly set
* Addressed rules:
  * asam.net:otx:1.0.0:zip_file.chk_002.type_safe_zip_file
  * asam.net:otx:1.0.0:zip_file.chk_001.type_safe_unzip_file

### state_machine_otx

* Description: Check if state_machine properties of input file are properly set
* Addressed rules:
  * asam.net:otx:1.0.0:state_machine.chk_001.no_procedure_realization
  * asam.net:otx:1.0.0:state_machine.chk_002.mandatory_target_state
  * asam.net:otx:1.0.0:state_machine.chk_003.no_target_state_for_completed_state
  * asam.net:otx:1.0.0:state_machine.chk_005.mandatory_transition
  * asam.net:otx:1.0.0:state_machine.chk_004.mandatory_trigger
  * asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state
