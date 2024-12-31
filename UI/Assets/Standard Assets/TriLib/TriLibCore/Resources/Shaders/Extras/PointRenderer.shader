Shader "Hidden/TriLib/PointRenderer"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
    
            #include "UnityCG.cginc"

            struct appdata
            {
                float2 id : TEXCOORD0;
            };

            struct v2f
            {
                float4 vertex : SV_POSITION;
                float4 color : TEXCOORD0;
            };

            Texture2D _ColorTex;
            Texture2D _PositionTex;
            uint _TextureResolution;
            float _PointSize;
            float _AspectRatio;

            static float2 _Offsets[4] = {
                {-1, -1 },
                {-1, 1 },
                {1, 1 },
                {1, -1 }
            };

            v2f vert (appdata v)
            {
                uint vertexID = floor(v.id.x);
    
                uint baseVertexID;
                uint cornerVertexID;
                if (vertexID == 0)
                {
                    baseVertexID = 0;
                    cornerVertexID = 0;
                }
                else
                {
                    baseVertexID = vertexID / 4;
                    cornerVertexID = vertexID % 4;
                }
    
                uint3 dataCoordinate = 0;
                if (baseVertexID == 0)
                {
                    dataCoordinate = 0;
                }
                else
                {
                    dataCoordinate.x = baseVertexID % _TextureResolution;
                    dataCoordinate.y = baseVertexID / _TextureResolution;
                }
    
                float3 sourcePosition = _PositionTex.Load(dataCoordinate).xyz;
        
                float4 clipPosition = UnityObjectToClipPos(sourcePosition);
                
                float2 adjustedOffset = _Offsets[cornerVertexID];
                adjustedOffset.x *= _PointSize / _AspectRatio;
                adjustedOffset.y *= _PointSize;
    
                clipPosition.xy += adjustedOffset;
    
                float4 color = _ColorTex.Load(dataCoordinate);
                
                v2f o;
                o.vertex = clipPosition;
                o.color = color;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                return i.color;
            }
            ENDCG
        }
    }
}
