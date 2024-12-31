Shader "Hidden/ShowSmooth"
{
     Properties {
        _MetallicGlossMap ("_MetallicGlossMap", 3D) = "black" {}
    }
    SubShader
    {
        Tags { "RenderType" = "Opaque" }
        LOD 100

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
                float4 vertex : SV_POSITION;
                float2 uv : TEXCOORD0;
            };

            sampler2D _MetallicGlossMap;
            float4 _MetallicGlossMap_ST;
            float4 _MetallicGlossMap_TexelSize;
            float _Glossiness;

            v2f vert(appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MetallicGlossMap);
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                return all(_MetallicGlossMap_TexelSize.zw <= 16) ? _Glossiness : tex2D(_MetallicGlossMap, i.uv).w;
            }
            ENDCG
        }
    }
}
