#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadowCoord;

struct Light {
    vec3 LightingPosition;
    vec3 LightingAmbience;
    vec3 LightingDiffusion;
    vec3 LightingSpecular;
};

uniform Light light;
uniform sampler2D Texture;
uniform vec3 CameraPosition;
uniform sampler2DShadow ShadowMap;
uniform vec2 Resolution;


float lookup(float ox, float oy) {
    vec2 pixelOffset = 1 / Resolution;
    return textureProj(ShadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w,
                                                     oy * pixelOffset.y * shadowCoord.w, 0.0, 0.0));
}


float getSoftShadowX4() {
    float shadow;
    float swidth = 1.5;  // shadow spread
    vec2 offset = mod(floor(gl_FragCoord.xy), 2.0) * swidth;
    shadow += lookup(-1.5 * swidth + offset.x, 1.5 * swidth - offset.y);
    shadow += lookup(-1.5 * swidth + offset.x, -0.5 * swidth - offset.y);
    shadow += lookup( 0.5 * swidth + offset.x, 1.5 * swidth - offset.y);
    shadow += lookup( 0.5 * swidth + offset.x, -0.5 * swidth - offset.y);
    return shadow / 4.0;
}



float getSoftShadowX16() {
    float shadow;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}


float getSoftShadowX64() {
    float shadow;
    float swidth = 0.6;
    float endp = swidth * 3.0 + swidth / 2.0;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 64;
}


float getShadow() {
    float shadow = textureProj(ShadowMap, shadowCoord);
    return shadow;
}


vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);

    vec3 ambient = light.LightingAmbience;

    vec3 lightDir = normalize(light.LightingPosition - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.LightingDiffusion;

    vec3 viewDir = normalize(CameraPosition - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.LightingSpecular;

    float shadow = getSoftShadowX16();

    return color * (ambient + (diffuse + specular) * shadow);
}


void main() {
    float gamma = 3.2;
    vec3 color = texture(Texture, uv_0).rgb;
    color = pow(color, vec3(gamma));

    color = getLight(color);

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 2.0);
}










