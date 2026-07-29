import shutil, os

def on_post_build(config, **kwargs):
    site = config["site_dir"]
    shutil.copy("schema/connoss_Software.jsonld",
                os.path.join(site, "connoss_Software.jsonld"))