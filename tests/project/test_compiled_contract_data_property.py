from populus.utils.filesystem import get_latest_mtime
from populus.utils.testing import load_contract_fixture


@load_contract_fixture('Math.sol')
def test_project_compiled_contract_data_with_no_default_env(project):
    assert 'Math' in project.compiled_contract_data
    assert 'bytecode' in project.compiled_contract_data['Math']
    assert 'bytecode_runtime' in project.compiled_contract_data['Math']
    assert 'abi' in project.compiled_contract_data['Math']

    compiled_contract_data_object_id = id(project.compiled_contract_data)

    assert id(project.compiled_contract_data) == compiled_contract_data_object_id


@load_contract_fixture('Math.sol')
def test_project_fill_contracts_cache(project):
    source_mtime = get_latest_mtime(project.get_all_source_file_paths())

    compiled_contract_data_object_id = id(project.compiled_contract_data)

    # fill with code from the future -> no recompilation
    project.fill_contracts_cache(project.compiled_contract_data, source_mtime + 10)
    assert id(project.compiled_contract_data) == compiled_contract_data_object_id

    # fill with code from the past -> recompilation
    project.fill_contracts_cache(project.compiled_contract_data, source_mtime - 10)
    assert not id(project.compiled_contract_data) == compiled_contract_data_object_id
