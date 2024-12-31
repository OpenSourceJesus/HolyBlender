Shader "Hidden/TriLib/SpecularDiffuseToAlbedo"
{
	SubShader
	{
		// No culling or depth
		Cull Off ZWrite Off ZTest Always

		Pass
		{
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag

			#include "UnityCG.cginc"

			struct appdata
			{
				float4 vertex : POSITION;
				float2 uv : TEXCOORD0;
			};

			struct v2f
			{
				float2 uv : TEXCOORD0;
				float4 vertex : SV_POSITION;
			};

			v2f vert(appdata v)
			{
				v2f o;
				o.vertex = UnityObjectToClipPos(v.vertex);
				o.uv = v.uv;
				return o;
			}

			sampler2D _DiffuseTexture;
			sampler2D _SpecularTexture;

			float getPerceivedBrightness(float3 linearColor)
			{
				float r = linearColor.x;
				float b = linearColor.y;
				float g = linearColor.z;
				return sqrt(0.299 * r * r + 0.587 * g * g + 0.114 * b * b);
			}

			float solveMetallic(float diffuseBrightness, float specularBrightness, float oneMinusSpecularStrength) {
				const float3 dielectricSpecular = float3(0.04, 0.04, 0.04);
				const float epsilon = 1e-6;
				specularBrightness = max(specularBrightness, dielectricSpecular.x);
				float a = dielectricSpecular.x;
				float b = diffuseBrightness * oneMinusSpecularStrength / (1.0 - dielectricSpecular.x) + specularBrightness - 2.0 * dielectricSpecular.x;
				float c = dielectricSpecular.x - specularBrightness;
				float D = b * b - 4.0 * a * c;
				return clamp((-b + sqrt(D)) / (2.0 * a), 0.0, 1.0);
			}

			float4 frag(v2f i) : SV_Target
			{
				const float3 dielectricSpecular = float3(0.04,0.04,0.04);
				const float epsilon = 1e-6;

				float4 diffuse = tex2D(_DiffuseTexture, i.uv);
				float3 specular = tex2D(_SpecularTexture, i.uv).xyz;

				float diffuseBrightness = getPerceivedBrightness(diffuse);
				float specularBrightness = getPerceivedBrightness(specular);

				float specularStrength = max(max(specular.x, specular.y), specular.z);
				float oneMinusSpecularStrength = 1.0 - specularStrength;

				float metallic = solveMetallic(diffuseBrightness, specularBrightness, oneMinusSpecularStrength);

				float3 baseColorFromDiffuse = diffuse * oneMinusSpecularStrength / ((1.0 - dielectricSpecular.x) * max(1.0 - metallic, epsilon));
				float3 baseColorFromSpecular = (specular - dielectricSpecular * (1.0 - metallic)) / max(metallic, epsilon);
				float3 baseColor = clamp(lerp(baseColorFromDiffuse, baseColorFromSpecular, metallic * metallic), 0.0, 1.0);

				return float4(baseColor, diffuse.w);
			}
			ENDCG
		}
	}
}
