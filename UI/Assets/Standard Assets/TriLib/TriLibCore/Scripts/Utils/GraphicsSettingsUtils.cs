using UnityEngine.Rendering;

namespace TriLibCore.Utils
{
    /// <summary>
    /// Represents a series of graphic settings utility methods.
    /// </summary>
    public static class GraphicsSettingsUtils
    {
        /// <summary>Returns <c>true</c> if the project is using the Standard Rendering Pipeline.</summary>
        public static bool IsUsingStandardPipeline => GraphicsSettings.defaultRenderPipeline == null;

        /// <summary>Returns <c>true</c> if the project is using the Universal Rendering Pipeline.</summary>
        public static bool IsUsingUniversalPipeline => GraphicsSettings.defaultRenderPipeline != null && (GraphicsSettings.defaultRenderPipeline.name.StartsWith("UniversalRenderPipeline") || GraphicsSettings.defaultRenderPipeline.name.StartsWith("UniversalRP") || GraphicsSettings.defaultRenderPipeline.name.StartsWith("URP"));

        /// <summary>Returns <c>true</c> if the project is using the HDRP Rendering Pipeline.</summary>
        public static bool IsUsingHDRPPipeline => GraphicsSettings.defaultRenderPipeline != null && GraphicsSettings.defaultRenderPipeline.name.Contains("HD");
    }
}
