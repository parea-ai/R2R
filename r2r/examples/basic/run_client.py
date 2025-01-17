import os
import uuid

from r2r.client import R2RClient

# Initialize the client with the base URL of your API
base_url = "http://localhost:8000"  # Change this to your actual API base URL
client = R2RClient(base_url)

print("Upserting entry to remote db...")
# Upsert a single entry

entry_response = client.add_entry(
    str(uuid.uuid5(uuid.NAMESPACE_DNS, "doc 1")),  # document_id
    {"txt": "This is a test entry"},
    {"tags": ["example", "test"]},
    do_upsert=True,
)
print(f"Upsert entry response:\n{entry_response}\n\n")


entry_response = client.add_entry(
    str(uuid.uuid5(uuid.NAMESPACE_DNS, "doc 1")),  # document_id
    {"txt": "This is a test entry"},
    {"tags": ["example", "test"]},
    do_upsert=False,
)
print(f"Copy same entry response:\n{entry_response}\n\n")


print("Upserting entries to remote db...")
# Upsert multiple entries
entries = [
    {
        "document_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "doc 2")),
        "blobs": {"txt": "Second test entry"},
        "metadata": {"tags": "bulk"},
    },
    {
        "document_id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "doc 3")),
        "blobs": {"txt": "Third test entry"},
        "metadata": {"tags": "example"},
    },
]
bulk_upsert_response = client.add_entries(entries, do_upsert=True)
print(f"Upsert entries response:\n{bulk_upsert_response}\n\n")

# Perform a search
print("Searching remote db...")
search_response = client.search("test", 5)
print(f"Search response:\n{search_response}\n\n")

print("Searching remote db with filter...")
# Perform a search w/ filter
filtered_search_response = client.search("test", 5, filters={"tags": "bulk"})
print(f"Search response w/ filter:\n{filtered_search_response}\n\n")

print("Deleting sample document in remote db...")
# Delete a document
response = client.filtered_deletion(
    "document_id", str(uuid.uuid5(uuid.NAMESPACE_DNS, "doc 2"))
)
print(f"Deletion response:\n{response}\n\n")

print("Searching remote db with filter after deletion...")
# Perform a search w/ filter after deletion
post_deletion_filtered_search_response = client.search(
    "test", 5, filters={"tags": "bulk"}
)
print(
    f"Search response w/ filter+deletion:\n{post_deletion_filtered_search_response}\n\n"
)

# Example file path for upload
# get file directory
current_file_directory = os.path.dirname(os.path.realpath(__file__))

file_path = os.path.join(current_file_directory, "test.pdf")

print(f"Uploading and processing file: {file_path}...")
# # Upload and process a file
pdf_document_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "pdf 1"))  # document_id
metadata = {"tags": ["example", "test"]}
upload_pdf_response = client.upload_and_process_file(
    pdf_document_id, file_path, metadata, None
)
print(f"Upload test pdf response:\n{upload_pdf_response}\n\n")

print("Searching remote db after upload...")
# Perform a search on this file
pdf_filtered_search_response = client.search(
    "what is a cool physics equation?",
    5,
    filters={"document_id": pdf_document_id},
)
print(
    f"Search response w/ uploaded pdf filter:\n{pdf_filtered_search_response}\n"
)


print("Performing RAG...")
# Perform a search on this file
pdf_filtered_search_response = client.rag_completion(
    "Are there any test documents?",
    5,
    filters={"document_id": pdf_document_id},
)
print(
    f"Search response w/ uploaded pdf filter:\n{pdf_filtered_search_response}\n"
)


print("Fetching logs after all steps...")
logs_response = client.get_logs()
print(f"Logs response:\n{logs_response}\n")

print("Fetching logs summary after all steps...")
logs_summary_response = client.get_logs_summary()
print(f"Logs summary response:\n{logs_summary_response}\n")
