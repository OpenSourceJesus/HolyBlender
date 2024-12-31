Shader "Hidden/TriLib/ApplyTransparency"
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

			sampler2D _TransparencyTexture;
			sampler2D _DiffuseTexture;
			int _HasTransparencyTexture;
			int _HasDiffuseTexture;

			float4 frag(v2f i) : SV_Target
			{
				float4 diffuse = _HasDiffuseTexture ? tex2D(_DiffuseTexture, i.uv) : float4(1.0,1.0,1.0,1.0);
				float alpha = _HasTransparencyTexture ? tex2D(_TransparencyTexture, i.uv).x : diffuse.w;
				return float4(diffuse.xyz, alpha);
			}
			ENDCG
		}
	}
}
