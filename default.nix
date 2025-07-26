{
  lib,
  buildPythonApplication,
  orjson,
  pydantic,
  wikipedia,
  pytestCheckHook,
  setuptools,
}:
buildPythonApplication {
  pname = "pycronyms";
  version = "0.0.1";
  pyproject = true;

  src = ./.;

  build-system = [ setuptools ];

  dependencies = [
    orjson
    pydantic
    wikipedia
  ];

  nativeCheckInputs = [ pytestCheckHook ];

  pythonImportsCheck = [ "pycronyms" ];

  meta = {
    license = lib.licenses.gpl3;
    mainProgram = "pycronyms";
  };
}
