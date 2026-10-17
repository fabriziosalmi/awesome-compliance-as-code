-- Query AWS S3 buckets lacking default server-side encryption at rest (DORA Art. 10 / SOC 2 CC6.1)
select
  name as bucket_name,
  region,
  server_side_encryption_configuration -> 'Rules' as encryption_rules,
  case
    when server_side_encryption_configuration is null then 'NON_COMPLIANT'
    else 'COMPLIANT'
  end as compliance_status,
  'DORA Art. 10 / SOC 2 CC6.1 - Encryption at Rest' as control_reference
from
  aws_s3_bucket
where
  server_side_encryption_configuration is null;
