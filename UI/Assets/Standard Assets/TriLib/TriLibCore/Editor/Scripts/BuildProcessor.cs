using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using TriLibCore.Mappers;
using UnityEditor;
using UnityEngine;
using Object = UnityEngine.Object;

namespace TriLibCore.Editor
{
    public class BuildProcessor
    {
        public static void OnPostprocessBuild(Dictionary<string, string> removedFromBuild)
        {
            RestoreAssets(removedFromBuild);
        }

        public static void OnPreprocessBuild(Dictionary<string, string> removedFromBuild)
        {
#if TRILIB_ENABLE_WEBGL_THREADS
            PlayerSettings.WebGL.threadsSupport = true;
#else
            PlayerSettings.WebGL.threadsSupport = false;
#endif
            if (!Application.isBatchMode)
            {
#if UNITY_WSA
            if (!PlayerSettings.WSA.GetCapability(PlayerSettings.WSACapability.RemovableStorage) && EditorUtility.DisplayDialog(
                    "TriLib", "TriLib cache system needs the [RemovableStorage] WSA Capacity enabled. Do you want to enable it now?", "Yes", "No"))
            {
                PlayerSettings.WSA.SetCapability(PlayerSettings.WSACapability.RemovableStorage, true);
            }
#endif
                var materialMapper = AssetLoader.GetSelectedMaterialMapper(true);
                if (materialMapper != null && materialMapper.UseShaderVariantCollection)
                {
                    var shaderVariantCollection = Resources.Load<ShaderVariantCollection>(materialMapper.ShaderVariantCollectionPath);
                    if (shaderVariantCollection != null)
                    {
                        if (!ShaderVariantCollectionUtils.IsShaderVariantCollectionPreloaded(shaderVariantCollection))
                        {
                            if (EditorUtility.DisplayDialog("TriLib", $"The selected Material Mapper [{materialMapper.name}] is using a Shader Variant Collection.\nThe Shader Variant Collection used by the Material Mapper is not included in the Graphic Settings preloaded Shaders.\nDo you want to include it now?", "Yes", "No"))
                            {
                                ShaderVariantCollectionUtils.AddShaderVariantCollectionToGraphicSettings(shaderVariantCollection);
                            }
                        }
                        if (
                            AssetExists(materialMapper.CutoutMaterialPreset) ||
                            AssetExists(materialMapper.MaterialPreset) ||
                            AssetExists(materialMapper.CutoutMaterialPresetNoMetallicTexture) ||
                            AssetExists(materialMapper.MaterialPresetNoMetallicTexture) ||
                            AssetExists(materialMapper.TransparentComposeMaterialPreset) ||
                            AssetExists(materialMapper.TransparentMaterialPreset) ||
                            AssetExists(materialMapper.TransparentComposeMaterialPresetNoMetallicTexture) ||
                            AssetExists(materialMapper.TransparentMaterialPresetNoMetallicTexture)
                        )
                        {
                            if (EditorUtility.DisplayDialog("TriLib", $"The selected Material Mapper [{materialMapper.name}] is using a Shader Variant Collection.\nYour build doesn't need the Material Mapper legacy materials.\nDo you want to remove them from the build?", "Yes", "No"))
                            {
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.CutoutMaterialPreset);
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.MaterialPreset);
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.CutoutMaterialPresetNoMetallicTexture);
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.MaterialPresetNoMetallicTexture);
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.TransparentComposeMaterialPreset);
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.TransparentMaterialPreset);
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.TransparentComposeMaterialPresetNoMetallicTexture);
                                RemoveAssetFromBuild(removedFromBuild, materialMapper.TransparentMaterialPresetNoMetallicTexture);
                            }
                        }
                    }
                }
            }
        }

        private static bool AssetExists(Object asset)
        {
            if (asset != null)
            {
                var assetPath = AssetDatabase.GetAssetPath(asset);
                return !string.IsNullOrEmpty(assetPath);
            }
            return false;
        }

        private static Action<BuildPlayerOptions> GetBuildPlayerHandler(out bool success)
        {
            var buildPlayerWindowType = typeof(BuildPlayerWindow);
            var buildPlayerHandlerField = buildPlayerWindowType.GetField("buildPlayerHandler", BindingFlags.NonPublic | BindingFlags.Static);
            if (buildPlayerHandlerField != null)
            {
                success = true;
                return buildPlayerHandlerField.GetValue(null) as Action<BuildPlayerOptions>;
            }
            success = false;
            return null;
        }

        [InitializeOnLoadMethod]
        private static void Initialize()
        {
            var buildPlayerHandler = GetBuildPlayerHandler(out var success);
            if (!success || buildPlayerHandler != null)
            {
                Debug.LogWarning("TriLib tried to register a 'build player handler', but there was a' build player handler' registered. Aborting.");
                return;
            }
            BuildPlayerWindow.RegisterBuildPlayerHandler(OnBuildPlayer);
        }

        private static void OnBuildPlayer(BuildPlayerOptions buildOptions)
        {
            var removedFromBuild = new Dictionary<string, string>();
            try
            {
                OnPreprocessBuild(removedFromBuild);
                BuildPlayerWindow.DefaultBuildMethods.BuildPlayer(buildOptions);
            }
            finally
            {
                OnPostprocessBuild(removedFromBuild);
            }
        }

        private static void RemoveAssetFromBuild(Dictionary<string, string> removedFromBuild, Object asset)
        {
            if (asset != null)
            {
                var assetPath = AssetDatabase.GetAssetPath(asset);
                if (!string.IsNullOrEmpty(assetPath))
                {
                    assetPath = $"{Application.dataPath}/../{assetPath}";
                    if (File.Exists(assetPath))
                    {
                        var tempPath = $"{assetPath}.tmp";
                        File.Move(assetPath, tempPath);
                        removedFromBuild.Add(assetPath, tempPath);
                    }
                }
            }
        }

        private static void RestoreAssets(Dictionary<string, string> removedFromBuild)
        {
            if (removedFromBuild.Count > 0)
            {
                foreach (var kvp in removedFromBuild)
                {
                    if (File.Exists(kvp.Value))
                    {
                        File.Move(kvp.Value, kvp.Key);
                    }
                }
                AssetDatabase.Refresh();
            }
        }
    }
}