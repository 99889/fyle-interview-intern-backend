def test_get_api_not_found(client, h_principal):
    response = client.get(
        '/noapi',
    )
    error_response = response.json
    assert response.status_code == 404
    print(error_response)
    assert error_response['error'] == 'NotFound'
