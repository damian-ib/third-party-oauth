import oauth_requests


def main():
    # 1. Request the request token
    request_token_response = oauth_requests.request_token()
    if not request_token_response.ok:
        raise Exception(
            "Failed to request token: {}".format(request_token_response.text)
        )
    request_token_response_data = request_token_response.json()
    request_token = request_token_response_data["oauth_token"]
    print("Request token:", request_token)
    # 2. Generate the authorization link and ask the user to authorize
    authorization_link = oauth_requests.generate_authorization_link(
        request_token=request_token
    )
    print(
        "Please open the following link in your browser to authrorize:",
        authorization_link,
    )
    verifier_token = input("Please enter the verifier token from the query params: ")
    # 3. Request the access token and access token secret
    access_token_response = oauth_requests.access_token(
        request_token=request_token,
        verifier_token=verifier_token,
    )
    if not access_token_response.ok:
        raise Exception(
            "Failed to request access token: {}".format(access_token_response.text)
        )
    access_token_response_data = access_token_response.json()
    access_token = access_token_response_data["oauth_token"]
    access_token_secret = access_token_response_data["oauth_token_secret"]
    print("Access token:", access_token)
    print("Access token secret:", access_token_secret)
    # 4. Request the live sesssion token and its expiration time
    (
        live_session_token,
        live_session_token_expires_ms,
    ) = oauth_requests.live_session_token(
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    print("Live session token:", live_session_token)
    print("Live session token expires:", live_session_token_expires_ms)
    # 5. Initialize the brokerage session
    brokerage_session_response = oauth_requests.init_brokerage_session(
        access_token=access_token,
        live_session_token=live_session_token,
    )
    if not brokerage_session_response.ok:
        raise Exception(
            "Failed to initialize brokerage session: {}".format(
                brokerage_session_response.text
            )
        )
    brokerage_session_response_data = brokerage_session_response.json()
    print("Brokerage session:", brokerage_session_response_data)
    # 6. Make API requests, for example request market data snapshot
    market_data_snapshot_response = oauth_requests.market_data_snapshot(
        access_token=access_token,
        live_session_token=live_session_token,
        conids=[265598],
        fields=[84, 86],
    )
    if not market_data_snapshot_response.ok:
        raise Exception(
            "Failed to request market data snapshot: {}".format(
                market_data_snapshot_response.text
            )
        )
    market_data_snapshot_response_data = market_data_snapshot_response.json()
    print("Market data snapshot:", market_data_snapshot_response_data)


if __name__ == "__main__":
    main()
