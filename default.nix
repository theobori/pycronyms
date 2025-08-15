{
  lib,
  buildPythonApplication,
  orjson,
  pydantic,
  wikipedia,
  pytestCheckHook,
  setuptools,
  setuptools-scm,
  thefuzz,
  matplotlib,
  pandas,
}:
buildPythonApplication {
  pname = "pycronyms";
  version = "0.0.1";
  pyproject = true;

  src = ./.;

  build-system = [
    setuptools
    setuptools-scm
  ];

  dependencies = [
    orjson
    pydantic
    wikipedia
    thefuzz
    matplotlib
    pandas
  ];

  nativeCheckInputs = [ pytestCheckHook ];

  pythonImportsCheck = [ "pycronyms" ];

  meta = {
    license = lib.licenses.mit;
    mainProgram = "pycronyms";
  };
}
