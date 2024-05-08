output "vpc_id" {
  value = module.vpc.vpc_id
}

output "instance_public_ips" {
  value = aws_instance.ubuntu.*.public_ip
}

output "azs" {
  value = data.aws_availability_zones.available.names

}
