from requests import request
from json import loads


SP_CURL_FORMAT = "https://api.spotify.com/v1/search?q={query}&type={type}&market={market}" \
                 "&limit={limit}&include_external=audio"
SP_HEAD_FORMAT = "Bearer {token}"

default_playlist = {"name": "Not Found", "external_urls": {"spotify": "https://open.spotify.com/browse/featured"}}


def search(keywords: str, token: str, type: str = "playlist", market: str = "US", limit: int = 10):
    r = request(method="GET",
                url=SP_CURL_FORMAT.format(query=keywords,
                                          type=type,
                                          market=market,
                                          limit=str(limit)),
                headers={"Authorization": SP_HEAD_FORMAT.format(token=token)})
    if int(r.status_code / 100) == 2:
        result = loads(r.text)
        try:
            first_playlist = result["playlists"]["items"][0]
        except IndexError:
            first_playlist = default_playlist
        return first_playlist["name"], first_playlist["external_urls"]["spotify"]


def main():
    print(search("David%20Bowie", "BQAUDjgn6uFrUJDkgdX8Q49BnUpvs_TwtEiWG8X4iN_wpu2XCQ9u-TjAsDJgwQ85CJTBmslWK23StgeI0PsPB9-jFAmg9_KWYxLBAU1_trBU-OutuHeCcIAcgDQUqzaH6SBp5HoFoHkHdDniWcL5Vg82pIGbsqrBFGF-2_8GE0wcJ50hS-6MfNjbkg"))


if __name__ == '__main__':
    main()
