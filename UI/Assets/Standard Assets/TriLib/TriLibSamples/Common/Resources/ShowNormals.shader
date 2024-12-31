Shader "Hidden/ShowNormals"
{
    SubShader
    {
        Tags { "RenderType"="Opaque" }
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
                float3 normal : NORMAL;
                float4 tangent : TANGENT;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float4 vertex : SV_POSITION;
                float2 uv : TEXCOORD0;
                float3x3 tbn : TEXCOORD1;
                float3 normal : NORMAL;
            };
        
            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);        
                o.uv = v.uv;
                float3 tangent = normalize(v.tangent.xyz - v.normal * dot(v.normal, v.tangent.xyz));
                float3 bitangent = cross(v.normal, tangent) * v.tangent.w;
                o.tbn = float3x3(tangent, bitangent, v.normal);
                o.normal = v.normal;
                return o;
            }

            sampler2D _BumpMap;
            float4 _BumpMap_TexelSize;

            float4 frag(v2f i) : SV_Target
            {
                float3 normal;
                if (all(_BumpMap_TexelSize.zw <= 16))
                {
                    normal = i.normal;
                } 
                else
                {
                    normal = tex2D(_BumpMap, i.uv).xyz;
                    normal = normal * 2.0 - 1.0;
                    normal = normalize(mul(normal, i.tbn));
                }
                normal = (normal + 1.0) / 2.0;
                return float4(normal, 1.0);
            }
            ENDCG
        }
    }
}
