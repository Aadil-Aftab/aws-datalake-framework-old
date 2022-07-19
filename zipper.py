import os
import shutil


def zip_utils(source_path, target_zip_path, base_dir=None):
    """
    method to zip a file in the source_path to a target_path
    """
    if base_dir:
        shutil.make_archive(
            base_name=target_zip_path,
            format="zip",
            root_dir=source_path,
            base_dir=base_dir,
        )
    else:
        shutil.make_archive(
            base_name=target_zip_path,
            format="zip",
            root_dir=source_path,
        )


root_dir = os.getcwd()
utils_zip_src_path = root_dir + f"/src"
utils_zip_target_path = root_dir + f"/dependencies/utils"
lambda_zip_src_path = root_dir + f"/src/lambda"
lambda_zip_target_path = root_dir + f"/lambda/lambda_function"
connector_zip_src_path = root_dir
connector_zip_target_path = root_dir + f"/dependencies/connector"
print("Zipping process started ....")
zip_utils(
    utils_zip_src_path, utils_zip_target_path, base_dir="utils"
)
zip_utils(lambda_zip_src_path, lambda_zip_target_path)
zip_utils(connector_zip_src_path, connector_zip_target_path, base_dir='connector')
print("Zipping process completed ....")
