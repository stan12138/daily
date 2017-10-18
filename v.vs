#version 330

layout (location=0) in vec3 position;
layout (location=1) in vec2 tex;
layout (location=2) in vec3 Normal;


out vec2 texc;
out vec3 normal;
out vec3 fragpos;


uniform mat4 model;
uniform mat4 modely;
uniform mat4 view;
uniform mat4 projection;


void main()
{
	
	gl_Position = projection*view*modely*model*vec4(position,1.0f);
	fragpos = vec3(modely*model*vec4(position,1.0f));
	texc = tex;
	mat3 normalm = mat3(transpose(inverse(modely*model)));
	normal = normalm*Normal;
	

}