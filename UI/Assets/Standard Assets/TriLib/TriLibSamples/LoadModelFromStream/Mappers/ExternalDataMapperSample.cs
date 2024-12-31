using System;
using System.IO;
using TriLibCore.Mappers;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a class that finds external resources at the given model base path.
    /// </summary>
    public class ExternalDataMapperSample : ExternalDataMapper
    {
        /// <summary>
        /// Tries to find the given external data source using the original resource filename and the context parameters.
        /// </summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="originalFilename">The source data original filename.</param>
        /// <param name="finalPath">The found data final Path.</param>
        /// <returns>The external data source Stream, if found. Otherwise <c>null</c>.</returns>
        public override Stream Map(AssetLoaderContext assetLoaderContext, string originalFilename, out string finalPath)
        {
            finalPath = $"{assetLoaderContext.BasePath}/{FileUtils.GetFilename(originalFilename)}";
            if (File.Exists(finalPath))
            {
                Debug.Log($"Found external file at: {finalPath}");
                return File.OpenRead(finalPath);
            }
            throw new Exception($"File {originalFilename} not found.");
        }
    }
}