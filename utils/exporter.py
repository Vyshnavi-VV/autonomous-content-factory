import zipfile
import os
import json
import tempfile


def export_campaign(content: dict, fact_sheet: dict) -> str:
    """
    Exports the full campaign kit as a ZIP file.
    Returns the path to the ZIP file.
    """

    tmp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(tmp_dir, "campaign_kit.zip")

    with zipfile.ZipFile(zip_path, "w") as zf:

        # Blog post
        blog_path = os.path.join(tmp_dir, "blog_post.txt")
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(content.get("blog", ""))
        zf.write(blog_path, "blog_post.txt")

        # Social media thread
        social_path = os.path.join(tmp_dir, "social_thread.txt")
        with open(social_path, "w", encoding="utf-8") as f:
            f.write(content.get("social", ""))
        zf.write(social_path, "social_thread.txt")

        # Email teaser
        email_path = os.path.join(tmp_dir, "email_teaser.txt")
        with open(email_path, "w", encoding="utf-8") as f:
            f.write(content.get("email", ""))
        zf.write(email_path, "email_teaser.txt")

        # Fact sheet
        fs_path = os.path.join(tmp_dir, "fact_sheet.json")
        with open(fs_path, "w", encoding="utf-8") as f:
            json.dump(fact_sheet, f, indent=2)
        zf.write(fs_path, "fact_sheet.json")

    return zip_path