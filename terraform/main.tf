module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "FrankfurtVPC"
  cidr = "10.16.0.0/16"

  azs            = data.aws_availability_zones.available.names
  public_subnets = ["10.16.0.0/20", "10.16.16.0/20", "10.16.32.0/20"]

  map_public_ip_on_launch = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

resource "aws_instance" "ubuntu" {
  count = 3

  ami                    = data.aws_ami.ubuntu22.id
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.auth.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  subnet_id = module.vpc.public_subnets[count.index]

  tags = {
    Name = "instance-${count.index}"
    Role = count.index == 0 ? "k3s_master" : "k3s_worker"
  }
}

resource "aws_security_group" "ec2_sg" {
  depends_on  = [module.vpc]
  name        = "ec2-sg"
  description = "Allow SSH inbound traffic"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "auth" {
  key_name   = "ec2-key-pair"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDRY5Qa5WxYmCxeN11yUE/fqSVEjMu9qd4br5CmAEpewjAO7jPKn36rKYhANMVmXX6eJ1cCHecNCsGA5p4sCWBzMIWGhFqejA1nAMqqQ4OLuxSaEcfVtUho1prfoZJ4t9/b+ZeKqbtCPqFhLOdct+sHfcLfvAoSGn3bgNmFzft4BUvNtXva0uvFQ4jfJHCUL84RB0yqXksfpBuGs3VZ/nCMhLjKBE49WJigMKUmTQcMzfX47/CLxyvJgD+xrNWtawFTkCOtuiCKdUKPpwNgpL68Zve+NoaYpl9ABp9V2V8r/M1y9ht6UYF7gPwUjPt3OnSG2f51siXrsmiM+0MINBp8YVx6rlILsPiTvF5D9ZSIKQE35/OZIq+sEla2kms8U2FEzjK7goQfpZJIflFZBDo7INj5qTMA8GjtGD24KP9ZyAoNm9ygH8FZ434gxk07ZOjikKVEVgOEWtIj0i/mTOG/Kpa6VyBLPuHswp8UYOhWlNZY1FxWpMbjlHoHJiFcWhtCPWO5H8I2C+kBHk2XtJnb3pAq+7Yts8uxQd6n2lrtmPxVsnU2M2RxEF0LrmHyeLmKXow9WDcjK4CllVNDlLFFbx5fNgg6UwCTHxHgDYiV0p1w0QiYQp4/jjbhFRImznJ4OPsf3xYaz7U8GqFXsALb6Yzj1XbD6gQYBV1B3fv9TQ== catdev@50ed3c3242ea"
}
