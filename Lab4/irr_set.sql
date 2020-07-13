CREATE TABLE IF NOT EXISTS "doc"."irr_set_hist" (
   "field_id" TEXT, 
   "setting_id" TEXT,
   "setting_type" TEXT,
   "max_sprinkle_dur" TEXT,
   "offset_bef_sprinkle" TEXT,
   "max_wind_speed" TEXT,
   "humid" REAL,
   "skip_sprinkle_from" TEXT,
   "skip_sprinkle_to" TEXT,
   "last_updated" TIMESTAMP WITH TIME ZONE
)
CLUSTERED INTO 4 SHARDS
WITH (
   "allocation.max_retries" = 5,
   "blocks.metadata" = false,
   "blocks.read" = false,
   "blocks.read_only" = false,
   "blocks.read_only_allow_delete" = false,
   "blocks.write" = false,
   column_policy = 'strict',
   "mapping.total_fields.limit" = 1000,
   max_ngram_diff = 1,
   max_shingle_diff = 3,
   number_of_replicas = '0-1',
   refresh_interval = 1000,
   "routing.allocation.enable" = 'all',
   "routing.allocation.total_shards_per_node" = -1,
   "translog.durability" = 'REQUEST',
   "translog.flush_threshold_size" = 536870912,
   "translog.sync_interval" = 5000,
   "unassigned.node_left.delayed_timeout" = 60000,
   "warmer.enabled" = true,
   "write.wait_for_active_shards" = 'ALL'
):
CREATE TABLE IF NOT EXISTS "doc"."irr_set_cust" (
   "field_id" TEXT,
   "setting_id" TEXT,
   "max_sprinkle_dur" TEXT,
   "offset_bef_sprinkle" TEXT,
   "max_wind_speed" TEXT,
   "humid" REAL,
   "skip_sprinkle_from" TEXT,
   "skip_sprinkle_to" TEXT,
   "last_updated" TIMESTAMP WITH TIME ZONE
)
CLUSTERED INTO 4 SHARDS
WITH (
   "allocation.max_retries" = 5,
   "blocks.metadata" = false,
   "blocks.read" = false,
   "blocks.read_only" = false,
   "blocks.read_only_allow_delete" = false,
   "blocks.write" = false,
   column_policy = 'strict',
   "mapping.total_fields.limit" = 1000,
   max_ngram_diff = 1,
   max_shingle_diff = 3,
   number_of_replicas = '0-1',
   refresh_interval = 1000,
   "routing.allocation.enable" = 'all',
   "routing.allocation.total_shards_per_node" = -1,
   "translog.durability" = 'REQUEST',
   "translog.flush_threshold_size" = 536870912,
   "translog.sync_interval" = 5000,
   "unassigned.node_left.delayed_timeout" = 60000,
   "warmer.enabled" = true,
   "write.wait_for_active_shards" = 'ALL'
):
CREATE TABLE IF NOT EXISTS "doc"."irr_set_comn" (
   "setting_id" TEXT,
   "max_sprinkle_dur" TEXT,
   "offset_bef_sprinkle" TEXT,
   "max_wind_speed" TEXT,
   "humid" REAL,
   "skip_sprinkle_from" TEXT,
   "skip_sprinkle_to" TEXT,
   "last_updated" TIMESTAMP WITH TIME ZONE
)
CLUSTERED INTO 4 SHARDS
WITH (
   "allocation.max_retries" = 5,
   "blocks.metadata" = false,
   "blocks.read" = false,
   "blocks.read_only" = false,
   "blocks.read_only_allow_delete" = false,
   "blocks.write" = false,
   column_policy = 'strict',
   "mapping.total_fields.limit" = 1000,
   max_ngram_diff = 1,
   max_shingle_diff = 3,
   number_of_replicas = '0-1',
   refresh_interval = 1000,
   "routing.allocation.enable" = 'all',
   "routing.allocation.total_shards_per_node" = -1,
   "translog.durability" = 'REQUEST',
   "translog.flush_threshold_size" = 536870912,
   "translog.sync_interval" = 5000,
   "unassigned.node_left.delayed_timeout" = 60000,
   "warmer.enabled" = true,
   "write.wait_for_active_shards" = 'ALL'
);
