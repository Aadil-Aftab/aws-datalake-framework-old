from awsglue.utils import getResolvedOptions
from utils.data_asset import DataAsset
from utils.comUtils import *
from utils.standardizationUtils import *
import sys
import time


spark = sql.SparkSession.builder.getOrCreate()


def get_global_config():
    config_file_path = "globalConfig.json"
    file = open(file=config_file_path, mode="r")
    config = json.load(file)
    file.close()
    return config


args = getResolvedOptions(sys.argv, ["source_path", "source_id", "asset_id", "exec_id"])
global_config = get_global_config()
start_time = time.time()
asset = DataAsset(args, global_config, run_identifier="data-standardization")
try:
    source_df = create_spark_df(
        spark,
        asset.source_file_path,
        asset.asset_file_type,
        asset.asset_file_delim,
        asset.asset_file_header,
        asset.logger,
    )
    assert source_df is not None
except Exception or AssertionError:
    asset.logger.write(message="Unable to read the data from the source")
    asset.update_data_catalog(data_standardization="Failed")
    asset.logger.write_logs_to_s3()

asset.update_data_catalog(data_standardization="In-Progress")
metadata = asset.get_asset_metadata()
source_df.printSchema()
result = run_data_standardization(source_df, metadata, asset.logger)
result.printSchema()
target_system_info = get_target_system_info(
    asset.fm_prefix, asset.target_id, asset.region, asset.logger
)
timestamp = get_timestamp(asset.source_path)
target_path = get_standardization_path(
    target_system_info, asset.asset_id, timestamp, asset.logger
)
try:
    assert result is not None
    result.repartition(1).write.parquet(target_path, mode="overwrite")
except AssertionError:
    asset.update_data_catalog(data_standardization="Failed")
    asset.logger.write(message="Encountered error while running data standardization")

asset.update_data_catalog(data_standardization="Completed")
end_time = time.time()
total_time_taken = float("{0:.2f}".format(end_time - start_time))
asset.logger.write(message=f"Time Taken = {total_time_taken} seconds")
asset.logger.write_logs_to_s3()
stop_spark(spark)