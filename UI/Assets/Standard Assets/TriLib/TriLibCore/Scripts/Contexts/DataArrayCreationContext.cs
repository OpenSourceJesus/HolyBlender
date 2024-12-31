using System.Collections.Generic;
using TriLibCore.Interfaces;
using UnityEngine;

namespace TriLibCore
{
#if UNITY_2020_2_OR_NEWER
    public class DataArrayCreationContext : IAssetLoaderContext, IAwaitable
    {
        public AssetLoaderContext Context { get; set; }
        public IList<IModel> Models = new List<IModel>();
        public Mesh[] Meshes;
        public Mesh.MeshDataArray DataArray;
        public bool Completed { get; set; }
    }
#endif
}