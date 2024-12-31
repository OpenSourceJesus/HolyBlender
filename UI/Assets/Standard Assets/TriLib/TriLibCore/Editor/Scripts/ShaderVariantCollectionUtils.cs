using UnityEditor;
using UnityEngine;

namespace TriLibCore.Editor
{
    /// <summary>
    /// Represents a class with Shader Variant Collection utility methods.
    /// </summary>
    public static class ShaderVariantCollectionUtils
    {
        /// <summary>
        /// Adds the given Shader Variant Collection to the Graphic Settings preloaded shaders.
        /// </summary>
        /// <param name="shaderVariantCollection">The Shader Variant Collection to add.</param>
        public static void AddShaderVariantCollectionToGraphicSettings(ShaderVariantCollection shaderVariantCollection)
        {
            var graphicSettingAssets = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/GraphicsSettings.asset");
            if (graphicSettingAssets != null && graphicSettingAssets.Length > 0)
            {
                var graphicsSettings = new SerializedObject(graphicSettingAssets[0]);
                var preloadedShaders = graphicsSettings.FindProperty("m_PreloadedShaders");
                preloadedShaders.InsertArrayElementAtIndex(preloadedShaders.arraySize);
                preloadedShaders.GetArrayElementAtIndex(preloadedShaders.arraySize - 1).objectReferenceValue = shaderVariantCollection;
                graphicsSettings.ApplyModifiedProperties();
            }
        }

        /// <summary>
        /// Returns whether the given Shader Variant Collection exists on the Graphic Settings preloaded shaders.
        /// </summary>
        /// <param name="shaderVariantCollection">The Shader Variant Collection to check for.</param>
        /// <returns>Whether the Shader Variant Collection exists on the Graphic Settings preloaded shaders.</returns>
        public static bool IsShaderVariantCollectionPreloaded(ShaderVariantCollection shaderVariantCollection)
        {
            var graphicSettingAssets = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/GraphicsSettings.asset");
            if (graphicSettingAssets != null && graphicSettingAssets.Length > 0)
            {
                var graphicsSettings = new SerializedObject(graphicSettingAssets[0]);
                var preloadedShaders = graphicsSettings.FindProperty("m_PreloadedShaders");
                for (var i = 0; i < preloadedShaders.arraySize; i++)
                {
                    if (preloadedShaders.GetArrayElementAtIndex(i).objectReferenceValue == shaderVariantCollection)
                    {
                        return true;
                    }
                }
                return false;
            }
            return true;
        }
    }
}