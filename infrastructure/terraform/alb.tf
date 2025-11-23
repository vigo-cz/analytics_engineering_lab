# Application Load Balancer

# ALB
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = var.environment == "prod" ? true : false

  tags = {
    Name = "${var.project_name}-alb-${var.environment}"
  }
}

# Target Groups
resource "aws_lb_target_group" "streamlit" {
  name        = "${var.project_name}-streamlit-${var.environment}"
  port        = var.container_port_streamlit
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  tags = {
    Name = "${var.project_name}-streamlit-tg-${var.environment}"
  }
}

resource "aws_lb_target_group" "jupyter" {
  name        = "${var.project_name}-jupyter-${var.environment}"
  port        = var.container_port_jupyter
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200,302"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  tags = {
    Name = "${var.project_name}-jupyter-tg-${var.environment}"
  }
}

resource "aws_lb_target_group" "metabase" {
  name        = "${var.project_name}-metabase-${var.environment}"
  port        = var.container_port_metabase
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/api/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  tags = {
    Name = "${var.project_name}-metabase-tg-${var.environment}"
  }
}

# HTTP Listener (with path-based routing)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  # Default action: forward to Streamlit
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.streamlit.arn
  }

  tags = {
    Name = "${var.project_name}-http-listener-${var.environment}"
  }
}

# Listener Rules for path-based routing
resource "aws_lb_listener_rule" "jupyter" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.jupyter.arn
  }

  condition {
    path_pattern {
      values = ["/jupyter/*"]
    }
  }
}

resource "aws_lb_listener_rule" "metabase" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 200

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.metabase.arn
  }

  condition {
    path_pattern {
      values = ["/metabase/*"]
    }
  }
}
