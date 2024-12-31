using TriLibCore.Mappers;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore.Samples
{
#pragma warning disable 649
    public static class AutodeskInteractiveMaterialsHelper
    {
        public static void Setup(ref AssetLoaderOptions assetLoaderOptions)
        {
            var autodeskInteractiveMaterialMapper = ScriptableObject.CreateInstance<AutodeskInteractiveStandardMaterialMapper>();
            if (autodeskInteractiveMaterialMapper != null)
            {
                if (assetLoaderOptions == null)
                {
                    assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions();
                }
                if (assetLoaderOptions.MaterialMappers == null)
                {
                    assetLoaderOptions.MaterialMappers = new MaterialMapper[] { autodeskInteractiveMaterialMapper };
                }
                else
                {
                    ArrayUtils.Add(ref assetLoaderOptions.MaterialMappers, autodeskInteractiveMaterialMapper);
                }
                assetLoaderOptions.LoadDisplacementTextures = true;
                autodeskInteractiveMaterialMapper.CheckingOrder = 10000;
            }
        }
    }
}