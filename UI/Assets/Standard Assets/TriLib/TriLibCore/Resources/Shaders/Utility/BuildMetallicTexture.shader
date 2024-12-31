Shader "Hidden/TriLib/BuildMetallicTexture"
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

			sampler2D _MetallicTexture;
			sampler2D _DiffuseTexture;
			sampler2D _SpecularTexture;
			sampler2D _GlossinessTexture;
			float3 _DefaultDiffuse;
			float3 _DefaultSpecular;
			float _DefaultRoughness;
			float _DefaultMetallic;
			float _ShininessExponent;
			int _HasMetallicTexture;
			int _HasDiffuseTexture;
			int _HasSpecularTexture;
			int _HasGlossinessTexture;
			int _HasDefaultRoughness;
			int _HasDefaultMetallic;
			int _UsingRoughness;
			int _MixTextureChannelsWithColors;
			int _MetallicComponentIndex;
			int _GlossinessComponentIndex;

			float GetGlossiness() {
				return 1 - (_HasDefaultRoughness > 0 ? _DefaultRoughness : 1);
			}

			// Reference:
			// https://docs.microsoft.com/en-us/azure/remote-rendering/reference/material-mapping
			float4 frag(v2f i) : SV_Target
			{
				const float dielectricSpecular = 0.04;

				float3 specularBase = _HasSpecularTexture > 0 ? tex2D(_SpecularTexture, i.uv).xyz * _DefaultSpecular : _DefaultSpecular;

				//Metalness
				float metalness;
				if (_HasMetallicTexture > 0) {
					metalness = tex2D(_MetallicTexture, i.uv)[_MetallicComponentIndex];
					if (_HasDefaultMetallic && _MixTextureChannelsWithColors > 0) {
						metalness *= _DefaultMetallic;
					}
				}
				else if (_HasSpecularTexture > 0)
				{
					float3 diffuseBase = _DefaultDiffuse;
					float diffuseBrightness = 0.299 * pow(diffuseBase.r, 2) + 0.587 * pow(diffuseBase.g, 2) + 0.114 * pow(diffuseBase.b, 2);
					float specularBrightness = 0.299 * pow(specularBase.r, 2) + 0.587 * pow(specularBase.g, 2) + 0.114 * pow(specularBase.b, 2);
					float specularStrength = max(specularBase.r, max(specularBase.g, specularBase.b));
					float oneMinusSpecularStrength = 1 - specularStrength;
					float A = dielectricSpecular;
					float B = (diffuseBrightness * (oneMinusSpecularStrength / (1 - A)) + specularBrightness) - 2 * A;
					float C = A - specularBrightness;
					float squareRoot = sqrt(max(0, B * B - 4 * A * C));
					float value = (-B + squareRoot) / (2 * A);
					metalness = clamp(value, 0, 1);
					if (_HasDefaultMetallic && _MixTextureChannelsWithColors > 0) {
						metalness *= _DefaultMetallic;
					}
				}
				else 
				{
					metalness = _DefaultMetallic;
				}

				//Glossiness
				float glossiness;
				if (_HasGlossinessTexture > 0) {
					glossiness = _UsingRoughness > 0 ? 1 - tex2D(_GlossinessTexture, i.uv)[_GlossinessComponentIndex] : tex2D(_GlossinessTexture, i.uv)[_GlossinessComponentIndex];
					if (_HasDefaultRoughness && _MixTextureChannelsWithColors > 0) {
						glossiness *= GetGlossiness();
					}
				}
				else if (_HasSpecularTexture > 0)
				{
					float specularIntensity = specularBase.r * 0.2125 + specularBase.g * 0.7154 + specularBase.b * 0.0721;
					glossiness = 1 - sqrt(2 / (_ShininessExponent * specularIntensity + 2));
					if (_HasDefaultRoughness && _MixTextureChannelsWithColors > 0) {
						glossiness *= GetGlossiness();
					}
				}
				else {
					glossiness = GetGlossiness();
				}

				return float4(metalness, metalness, metalness, glossiness);
			}
			ENDCG
		}
	}
}
