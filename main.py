import csv
import tkinter as tk
from bs4 import BeautifulSoup
import requests


def create_gui():
    """Creates and displays the Tkinter GUI window."""

    root = tk.Tk()
    root.title("Code Generation")

    # Input label and entry
    info_label = tk.Label(root, text="CSV file path (leave blank for existing 'scraped_code.csv'):")
    info_label.grid(row=0, column=0)
    csv_path_entry = tk.Entry(root, width=50)
    csv_path_entry.grid(row=0, column=1)

    # Button for scraping code
    scrape_button = tk.Button(root, text="Scrape Existing URLs", command=lambda: scrape_existing(csv_path_entry, output_text))
    scrape_button.grid(row=1, column=0, columnspan=2)

    # Output text box
    output_text = tk.Text(root, height=10, width=50)
    output_text.grid(row=2, column=0, columnspan=2)

    root.mainloop()


def scrape_existing(csv_path_entry, output_text):
    """Scrapes code snippets from URLs listed in a CSV file."""

    csv_path = csv_path_entry.get() or "scraped_code.csv"
    selector = "code"  # Adjust the selector as needed

    try:
        url_snippets = read_url_snippets(csv_path)

        scraped_count = 0
        for url, snippet in url_snippets:
            if not snippet:  # Skip URLs with existing snippets
                new_snippets = scrape_code_snippets(url, selector)
                if new_snippets:
                    # Update the CSV file with the new snippets
                    update_csv_snippet(csv_path, url, new_snippets)
                    scraped_count += len(new_snippets)
                    output_text.insert("end", f"Scraped {len(new_snippets)} snippets from {url}\n")
                else:
                    output_text.insert("end", f"No new snippets found on {url}\n")

        output_text.insert("end", f"\nTotal scraped snippets: {scraped_count}")

    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert("end", f"Error scraping code: {e}")


def read_url_snippets(csv_path):
    """Reads url and code snippet pairs from a CSV file."""

    snippets = []
    with open(csv_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header row
        for row in reader:
            url = row[0]
            snippet = row[1] if len(row) > 1 else None
            snippets.append((url, snippet))
    return snippets


def scrape_code_snippets(url, selector):
    """Scrapes all code snippets from the given URL using the specified selector."""

    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    code_blocks = soup.select(selector)

    snippets = []
    for code_block in code_blocks:
        code_text = code_block.get_text(strip=True)
        if code_text:
            snippets.append(code_text)

    return snippets


def update_csv_snippet(csv_path, url, new_snippets):
    """Updates the code snippet for a specific URL in a CSV file.

    Preserves existing snippets and handles empty snippets.

    Args:
        csv_path (str): Path to the CSV file.
        url (str): URL to identify the row to update.
        new_snippets (list[str]): List of new code snippets to write.
    """

    new_content = []
    with open(csv_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != url:
                new_content.append(row)
            else:
                # If updating existing snippet, preserve any previous snippets
                previous_snippet = "\n".join(row[1:]) if len(row) > 1 else ""
                updated_snippet = "\n".join([previous_snippet, *new_snippets])
                new_content.append([url, updated_snippet])

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Code Snippet"])
        writer.writerows(new_content)


if __name__ == "__main__":
    create_gui()
