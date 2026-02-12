import requests
import sys

BASE_URL_ALL = "https://restcountries.com/v3.1/all"
BASE_URL_NAME = "https://restcountries.com/v3.1/name/{}"
FIELDS = "name,capital,population,continents"


def normalize_country_name(name):
    if not name or not name.strip():
        return None
    return name.strip().replace("_", " ").title()


def get_country_info(country_name=None):

    normalized_name = normalize_country_name(country_name)

    if normalized_name:
        url = BASE_URL_NAME.format(normalized_name)
    else:
        url = BASE_URL_ALL

    try:
        response = requests.get(
            url,
            params={"fields": FIELDS},
            timeout=10
        )
        response.raise_for_status()
        countries = response.json()

        if not isinstance(countries, list):
            print("Unexpected API response format")
            return

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    for country in countries:
        common_name = country.get("name", {}).get("common", "N/A")
        capital = ", ".join(country.get("capital", ["N/A"]))
        population = country.get("population", "N/A")
        continents = ", ".join(country.get("continents", ["N/A"]))

        print(f"Country: {common_name}")
        print(f"Capital: {capital}")
        print(f"Population: {population}")
        print(f"Continents: {continents}")
        print("-" * 40)


if __name__ == "__main__":
    arg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    get_country_info(arg)
