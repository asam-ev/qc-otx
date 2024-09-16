# Checker bundle: otxBundle

* Build version:  0.1.0
* Description:    OTX checker bundle

## Parameters

* InputFile 

## Checkers

### check_asam_otx_core_chk_001_document_name_matches_filename

* Description: For OTX documents stored in a file system, the attribute name of the <otx> root element should match the filename of the containing file (without the extension '.otx').
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_001.document_name_matches_filename

### check_asam_otx_core_chk_002_document_name_package_uniqueness

* Description: The value of the <otx> attribute name shall be unique within the scope of all OTX documents belonging to the same package.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_002.document_name_package_uniqueness

### check_asam_otx_core_chk_003_no_dead_import_links

* Description: Imported OTX documents (referenced by package name and document name via <import> elements) should exist and should be accessible.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_003.no_dead_import_links

### check_asam_otx_core_chk_004_no_unused_imports

* Description: An imported OTX document should be used at least once in the importing document.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_004.no_unused_imports

### check_asam_otx_core_chk_005_no_use_of_undefined_import_prefixes

* Description: If an imported name is accessed by prefix in an OtxLink type attribute, the corresponding prefix definition shall exist in an <import> element.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_005.no_use_of_undefined_import_prefixes

### check_asam_otx_core_chk_006_match_of_imported_document_data_model_version

* Description: An imported OTX document (imported by an <import> element) shall be bound to the same data model version as the importing document.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_006.match_of_imported_document_data_model_version

### check_asam_otx_core_chk_007_have_specification_if_no_realisation_exists

* Description: For all elements with specification and realisation parts in an OTX document: if there is no <realisation> given, the according <specification> element should exist and have content (no empty string).
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_007.have_specification_if_no_realisation_exists

### check_asam_otx_core_chk_008_public_main_procedure

* Description: he value of <procedure> attribute visibility shall always be 'PUBLIC' if the procedure name is 'main'.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_008.public_main_procedure

### check_asam_otx_core_chk_009_mandatory_constant_initialization

* Description: Constant declarations shall always be initialized.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_009.mandatory_constant_initialization

### check_asam_otx_core_chk_010_unique_node_names

* Description: The value of a nodes name attribute should be unique among all nodes in a procedure.
* Addressed rules:
  * asam.net:otx:1.0.0:core.chk_010.unique_node_names

### check_asam_otx_data_type_chk_001_accessing_structure_elements

* Description: Accessing structure elements is only allowed via StepByName using matching string literals.
* Addressed rules:
  * asam.net:otx:1.0.0:data_type.chk_001.accessing_structure_elements

### check_asam_otx_data_type_chk_008_correct_target_for_structure_element

* Description: When referring to a structure element, an existing <element> name of the referenced StructureSignature shall be used.
* Addressed rules:
  * asam.net:otx:1.0.0:data_type.chk_008.correct_target_for_structure_element

### check_asam_otx_zip_file_chk_002_type_safe_zip_file

* Description: In a ZipFile action, the list described by ListTerm <extensions> shall have a data type of <String>.
* Addressed rules:
  * asam.net:otx:1.0.0:zip_file.chk_002.type_safe_zip_file

### check_asam_otx_zip_file_chk_001_type_safe_unzip_file

* Description: In an UnZipFile action, the list described by ListTerm <extensions> shall have a data type of <String>.
* Addressed rules:
  * asam.net:otx:1.0.0:zip_file.chk_001.type_safe_unzip_file

### check_asam_otx_state_machine_chk_001_no_procedure_realization

* Description: A StateMachineProcedure shall not have a ProcedureRealisation.
* Addressed rules:
  * asam.net:otx:1.0.0:state_machine.chk_001.no_procedure_realization

### check_asam_otx_state_machine_chk_002_mandatory_target_state

* Description: Each state except the completed state shall have a target state.
* Addressed rules:
  * asam.net:otx:1.0.0:state_machine.chk_002.mandatory_target_state

### check_asam_otx_state_machine_chk_003_no_target_state_for_completed_state

* Description: After finishing the completed state the procedure is finished and shall return to the caller. Therefore the completed state shall not have a target state.
* Addressed rules:
  * asam.net:otx:1.0.0:state_machine.chk_003.no_target_state_for_completed_state

### check_asam_otx_state_machine_chk_005_mandatory_transition

* Description: Each state except the completed state shall have at least one transition.
* Addressed rules:
  * asam.net:otx:1.0.0:state_machine.chk_005.mandatory_transition

### check_asam_otx_state_machine_chk_004_mandatory_trigger

* Description: Each state except the completed state shall have at least one trigger.
* Addressed rules:
  * asam.net:otx:1.0.0:state_machine.chk_004.mandatory_trigger

### check_asam_otx_state_machine_chk_006_distinguished_initial_and_completed_state

* Description: The values of the mandatory initialState and optional completedState attributes shall be distinguished.
* Addressed rules:
  * asam.net:otx:1.0.0:state_machine.chk_006.distinguished_initial_and_completed_state
