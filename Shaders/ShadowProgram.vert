#version 330 core

//Unused
layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;

layout (location = 2) in vec3 in_position;

uniform mat4 MatrixProjection;
uniform mat4 MatrixViewLight;
uniform mat4 MatrixModel;

void main() {
    //Unused
    vec3 in_normal = in_normal;
    vec2 in_texcoord_0 = in_texcoord_0;
    mat4 MatrixViewProjection = MatrixProjection * MatrixViewLight * MatrixModel;
    gl_Position = MatrixViewProjection * vec4(in_position, 1.0);
}
