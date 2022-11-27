def test_initialize_database(cli_test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the 'flask init_db' command is called from the command line
    THEN check the response is valid
    """
    output = cli_test_client.invoke(args=['init_db'])
    assert output.exit_code == 0
    assert 'Initialized the database!' in output.output
