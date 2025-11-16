import pytest
from jsonschema import validate
import requests
import schemas

base_url = "https://reqres.in"
endpoint_users = "/api/users"
endpoint_register = "/api/register"
endpoint_login = "/api/login"
endpoint_unknown = "/api/unknown"
header_auth = {"x-api-key": "reqres-free-v1"}


def test_method_response_status_get_list_users():
    response = requests.get(base_url + endpoint_users,
                            headers=header_auth,
                            params={"page": 2})
    assert response.status_code == 200


def test_method_response_body_schema_post_users():
    response = requests.post(base_url + endpoint_users,
                             headers=header_auth,
                             data={
                                 "name": "morpheus",
                                 "job": "leader"
                             })
    # Переставил местами. Не совсем понятно в чем отличие - почему надо сначала проверять статус-код, а потом схему?
    assert response.status_code == 201
    validate(response.json(), schema=schemas.response_post_users_ok)


def test_method_response_status_delete_users():
    response = requests.delete(base_url + endpoint_users + "/2",
                               headers=header_auth)
    assert response.status_code == 204


def test_method_response_body_schema_put_users():
    response = requests.put(base_url + endpoint_users + "/2",
                            headers=header_auth,
                            data={
                               "name": "morpheus",
                               "job": "zion resident"
                            })
    assert response.status_code == 200
    validate(response.json(), schema=schemas.response_put_users_ok)


def test_negative_method_response_without_auth_key_put_users():
    response = requests.put(base_url + endpoint_users + "/2",
                            data={
                                "name": "morpheus",
                                "job": "zion resident"
                            })
    assert response.status_code == 401
    validate(response.json(), schema=schemas.response_put_users_error_api_key)


def test_method_response_status_post_register():
    response = requests.post(base_url + endpoint_register,
                             headers=header_auth,
                             data={
                                "email": "sydney@fife"
                             })
    assert response.status_code == 400


def test_method_response_status_get_unknown():
    response = requests.get(base_url + endpoint_unknown + "/23",
                            headers=header_auth)
    assert response.status_code == 404


def test_method_response_schema_patch_users():
    response = requests.patch(base_url + endpoint_users + "/2",
                              headers=header_auth,
                              data={
                                  "name": "morpheus",
                                  "job": "zion resident"
                              })
    assert response.status_code == 200
    validate(response.json(), schema=schemas.response_patch_users_ok)


"""
        С точки зрения тестирования метода без ответа, то у меня был тест test_method_response_status_delete_users
    Думал его достаточно. Правда я там проверял только статус-код и отсутствие ответа - не проверял.
    На лекции вопрос проверки отсутствия ответа я как-то не припомню. Поэтому посмотрел как этот вопрос решили 
    другие ученики. Их версия мне показалась не соответствующей условиям - у них проверка идет на ответ состоящий
    из пустого json = {}. Но это же не соответствует условию. Пустой json в ответе == ответ не пустой. На мой взгляд 
    надо брать метод у которого в ответе body вообще пустое и проверять это. Согласно тз.
    Поэтому я сделал тест test_method_response_no_body_delete_users. 
    
        Не уверен, что это оптимальное решение, но что смог придумать. Если подскажите лучше вариант - буду благодарен.
    
        Ну и на всякий случай, что бы три раза не вставать - приделал тест 
    test_method_response_empty_json_in_body_get_unknown с проверкой на пустой json в ответе
"""


def test_method_response_no_body_delete_users():
    response = requests.delete(base_url + endpoint_users + "/2",
                               headers=header_auth)
    assert response.status_code == 204
    with pytest.raises(ValueError):
        data = response.json()


def test_method_response_empty_json_in_body_get_unknown():
    response = requests.get(base_url + endpoint_unknown + "/23",
                            headers=header_auth)
    assert response.status_code == 404
    assert response.json() == {}
