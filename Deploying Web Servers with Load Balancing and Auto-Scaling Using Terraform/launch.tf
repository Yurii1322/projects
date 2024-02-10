resource "aws_key_pair" "key-key" {
  key_name   = "key"
  public_key = file(var.PUB_KEY)
}

#Launch template
resource "aws_launch_configuration" "webserver-launch-config" {
  name_prefix     = "webserver-launch-config"
  image_id        = var.AMIS[var.REGION]
  instance_type   = "t2.micro"
  key_name        = aws_key_pair.key-key.key_name
  security_groups = [aws_security_group.webserver_sg.id]

  root_block_device {
    volume_type = "gp2"
    volume_size = 10
    encrypted   = true
  }

  ebs_block_device {
    device_name = "/dev/sdf"
    volume_type = "gp2"
    volume_size = 5
    encrypted   = true
  }

  lifecycle {
    create_before_destroy = true
  }

  user_data = base64encode(file("${path.module}/init.sh"))
}