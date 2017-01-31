from addok.batch import process_documents
from addok.core import search


def test_process_should_index_by_default(factory):
    doc = factory(skip_index=True, name="Melicocq")
    assert not search("Mélicocq")
    process_documents(doc.copy())
    assert search("Melicocq")


def test_process_should_deindex_if_action_is_given(factory):
    doc = factory(name="Mélicocq")
    assert search("Mélicoq")
    process_documents({"_action": "delete", "id": doc["id"]})
    assert not search("Mélicoq")


def test_process_should_update_if_action_is_given(factory):
    doc = factory(name="rue de l'avoine")
    assert search("rue")
    doc["_action"] = "update"
    doc["name"] = "avenue de l'avoine"
    process_documents(doc.copy())
    assert search("avenue")
    assert not search("rue")
