using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

namespace TriLibCore.Extras
{
    /// <summary>
    /// Represents a class that renders point clouds and is compatible with every Unity platform.
    /// </summary>
    public class PointRenderer : MonoBehaviour
    {
        /// <summary>
        /// The size of each rendered point.
        /// </summary>
        public float PointSize = 0.01f;

        /// <summary>
        /// The texture containing the mesh colors.
        /// </summary>
        private Texture2D _colorTexture;

        /// <summary>
        /// The texture containing the mesh positions.
        /// </summary>
        private Texture2D _positionTexture;

        /// <summary>
        /// The material used to render the point cloud.
        /// </summary>
        public Material Material { get; private set; }

        /// <summary>
        /// The mesh created to draw the point cloud.
        /// This mesh is needed to overcome the lack of the `SV_VertexID` semantic in WebGL.
        /// </summary>
        public Mesh Mesh { get; private set; }

        /// <summary>
        /// Initializes the point renderer data with the given mesh data.
        /// </summary>
        /// <param name="mesh">The mesh to draw the points from.</param>
        public void Initialize(Mesh mesh)
        {
            if (mesh == null)
            {
                throw new ArgumentNullException(nameof(mesh));
            }

            var textureResolution = Mathf.CeilToInt(Mathf.Sqrt(mesh.vertexCount));

            _colorTexture = new Texture2D(textureResolution, textureResolution, TextureFormat.RGBA32, false);
            var colorData = _colorTexture.GetRawTextureData<Color32>();

            _positionTexture = new Texture2D(textureResolution, textureResolution, TextureFormat.RGBAFloat, false);
            var positionData = _positionTexture.GetRawTextureData<Vector4>();

            var vertices = mesh.vertices;
            var colors = mesh.colors32;
            if (colors.Length < vertices.Length)
            {
                colors = new Color32[vertices.Length];
                for (var i = 0; i < colors.Length; i++)
                {
                    colors[i] = new Color32(255, 255, 255, 255);
                }
            }

            for (var i = 0; i < mesh.vertexCount; i++)
            {
                colorData[i] = colors[i];
                positionData[i] = vertices[i];
            }

            _colorTexture.Apply(false, true);
            _positionTexture.Apply(false, true);

            Material = new Material(Shader.Find("Hidden/TriLib/PointRenderer"));
            Material.SetTexture("_ColorTex", _colorTexture);
            Material.SetTexture("_PositionTex", _positionTexture);
            Material.SetInt("_TextureResolution", textureResolution);
            
            Mesh = CreateCompatibleMesh(MeshTopology.Quads, mesh.vertexCount * 4);
        }

        /// <summary>
        /// Creates a new mesh to simulate DrawProceduralNow. 
        /// </summary>
        /// <param name="meshTopology">The mesh topology.</param>
        /// <param name="vertexCount">The final vertex count.</param>
        /// <returns>The created mesh.</returns>
        private static Mesh CreateCompatibleMesh(MeshTopology meshTopology, int vertexCount)
        {
            var mesh = new Mesh();
            mesh.subMeshCount = 1;
            mesh.indexFormat = vertexCount > ushort.MaxValue ? IndexFormat.UInt32 : IndexFormat.UInt16;
            mesh.vertices = new Vector3[vertexCount];
            var uv = new Vector2[vertexCount];
            for (var i = 0; i < vertexCount; i++)
            {
                uv[i] = new Vector2(i, 0);
            }
            mesh.uv = uv;
            var indices = new List<int>(vertexCount);
            switch (meshTopology)
            {
                case MeshTopology.Triangles:
                    for (var i = 0; i < vertexCount; i += 3)
                    {
                        indices.Add(i + 0);
                        indices.Add(i + 1);
                        indices.Add(i + 2);
                    }
                    break;
                case MeshTopology.Quads:
                    for (var i = 0; i < vertexCount; i += 4)
                    {
                        indices.Add(i + 0);
                        indices.Add(i + 1);
                        indices.Add(i + 2);
                        indices.Add(i + 3);
                    }
                    break;
                case MeshTopology.Lines:
                    for (var i = 0; i < vertexCount; i += 2)
                    {
                        indices.Add(i + 0);
                        indices.Add(i + 1);
                    }
                    break;
                case MeshTopology.LineStrip:
                case MeshTopology.Points:
                    for (var i = 0; i < vertexCount; i++)
                    {
                        indices.Add(i);
                    }
                    break;
                default:
                    throw new ArgumentOutOfRangeException(nameof(meshTopology), meshTopology, null);
            }
            mesh.SetIndices(indices, 0, indices.Count, meshTopology, 0);
            mesh.UploadMeshData(true);
            return mesh;
        }

        /// <summary>
        /// Renders the point cloud using the previously created mesh.
        /// </summary>
        private void OnRenderObject()
        {
            var aspectRatio = (float)Screen.width / Screen.height;
            Material.SetFloat("_AspectRatio", aspectRatio);
            Material.SetFloat("_PointSize", PointSize);
            Material.SetPass(0);
            Graphics.DrawMeshNow(Mesh, transform.localToWorldMatrix);
        }
    }
}