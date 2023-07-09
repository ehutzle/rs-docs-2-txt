from bs4 import BeautifulSoup
import requests


def extract_items(base_url):
    # Get the HTML content of the page
    response = requests.get(base_url)

    # If request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section with id "main-content"
        section = soup.find(id="main-content")

        # Create an empty dictionary to hold the data
        data = {}

        # Iterate over the h2 elements in the section
        for h2 in section.find_all('h2'):
            # Get the name of the category (structs, enums, etc.)
            category = h2.get_text().lower()
            data[category] = {}

            # Get the ul that immediately follows the h2
            ul = h2.find_next_sibling('ul')

            # Iterate over the li elements in the ul
            for li in ul.find_all('li'):
                # Get the <a> element in the li
                a = li.find('a')

                # Get the name and href of the item
                name = a.get_text()
                href = a.get('href')

                # Add the item to the data dictionary
                data[category][name] = href

        return data

    else:
        return f"Unable to reach the website. HTTP status code: {response.status_code}"


def extract_text_from_page(base_url, href):
    # Get the HTML content of the page
    page_url = base_url + href
    response = requests.get(page_url)

    # If request was successful
    if response.status_code == 200:

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section with id "main-content"
        section = soup.find(id="main-content")

        if section:
            # Extract the text
            text = section.get_text()

            return text

        else:
            return "Section with id 'main-content' was not found."

    else:
        return f"Unable to reach the website. HTTP status code: {response.status_code}"


def loop_through_items(base_url, data):
    master_text = ""
    for category, items in data.items():
        for name, href in items.items():
            text = extract_text_from_page(base_url, href)
            master_text += f'{text}\n\n'
    master_text = master_text[:-4]
    return master_text


def get_crate_name(base_url):
    split_url = base_url.split("/")
    crate_name = split_url[3]
    return crate_name


def write_to_file(base_url, master_text):
    crate_name = get_crate_name(base_url)
    with open(f'{crate_name}.txt', 'w', encoding='utf-8') as f:
        f.write(master_text)


def main(base_url):
    data = extract_items(base_url)
    master_text = loop_through_items(base_url, data)
    write_to_file(base_url, master_text)
    return master_text


if __name__ == "__main__":
    url = 'https://docs.rs/redb/latest/redb/'
    main(base_url=url)
