var canvas = {};
canvas.obj = document.getElementById("window");
canvas.width = canvas.obj.width;//getBoundingClientRect().width;
canvas.height = canvas.obj.height;//getBoundingClientRect().height;
ctx = canvas.obj.getContext("2d");

ctx.fillRect(0,0,100,100);
ctx.strokeRect(100,100,100,100);
ctx.beginPath()
ctx.arc(250,250,100,0,Math.PI*2,false);
ctx.fillStyle = "#ff00ff"
ctx.fill();

class Ball
{
	constructor(x)
	{
		this.x = x;
		this.y = canvas.height;
		this.color = ran_color();//`hsla(${360 * Math.random() | 0},80%,60%,1)`;
		this.origin_y = canvas.height;
		this.end_y = 200*Math.random();
		this.r = 2;
		this.v = -3;
		this.particle = [];
		this.state = 1;
	}

	move()
	{
		if(this.y>this.end_y) this.y += this.v;
		else
		{
			this.state = 2;
			this.create(200);
		}
	}

	render()
	{
		this.move();
		ctx.fillStyle = this.color;
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.r, 0, Math.PI*2, false);
		ctx.fill();
	}

	create(num)
	{
		for(var i=0; i<num; i++)
		{
			var p = new firework(this.x, this.y, 1, this.color);
			this.particle.push(p);
		}
	}

}

class firework
{
	constructor(x,y,r,color)
	{
		this.x = x;
		this.y = y;
		this.r = r;
		this.color = color;
		this.v = 2*Math.random();
		this.angle = Math.PI*2*Math.random();
		this.vx = Math.cos(this.angle)*this.v;
		this.vy = Math.sin(this.angle)*this.v;
		this.origin_vx = this.vx;
	}

	move()
	{
		this.x += this.vx;
		this.y += this.vy;
		this.vy += 0.02;

		this.vx *= 0.98;
		this.vy *= 0.98;

	}

	render()
	{
		this.move();
		ctx.fillStyle = this.color+judge_opacity(this.origin_vx, this.vx);
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.r, 0, Math.PI*2, false);
		ctx.fill();
	}
}

var balls = [];
for(var i=0; i<10; i++)
{
	balls.push(new Ball(Math.random()*canvas.width));
}

requestAnimationFrame(draw);

function draw()
{
	ctx.fillStyle = 'rgba(0,0,0,0.2)';
	ctx.fillRect(0,0,canvas.width,canvas.height);
	var len1 = balls.length;
	for(var i=0; i<len1; i++)
	{
		var b = balls[i];
		var delete_num = 0;
		if(b.state==1) b.render();
		else
		{
			var len = b.particle.length;
			for(var j=0; j<len; j++)
			{
				b.particle[j].render();
				delete_num += should_delete(b.particle[j].vx);
			}
			if(delete_num>130)
			{
				balls.splice(i,1,new Ball(Math.random()*canvas.width));
			}
		}
	}
	requestAnimationFrame(draw);
}

function rgb2hex(r, g, b)
{
	var hex = "#" + ((1<<24) + (r<<16) + (g <<8) + b).toString(16).slice(1);
    return hex;
}

function ran_color()
{
	var r = Math.round(Math.random()*256);
	var g = Math.round(Math.random()*256);
	var b = Math.round(Math.random()*256);
	return rgb2hex(r,g,b);
}

function judge_opacity(origin_v,v)
{
	//if(v<(origin_v/2))
	//{
	//	return ((1<<8)+Math.round(v*255)).toString(16).slice(1);
	//}
	//else return "ff";
	return ((1<<8)+Math.min(Math.round(v*255)*2,256)).toString(16).slice(1);
}

function should_delete(v)
{
	if(Math.min(Math.round(v*255)*2,256)<10) return 1;
	else return 0;
}