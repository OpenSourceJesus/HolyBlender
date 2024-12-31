#pragma warning disable 672

using System;
using System.IO;
using TriLibCore.Interfaces;
using TriLibCore.Mappers;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a class that finds textures at the given model base path.
    /// </summary>
    public class TextureMapperSample : TextureMapper
    {
        /// <summary>Tries to retrieve a Stream to the Texture native data based on the given context.</summary>
        public override void Map(TextureLoadingContext textureLoadingContext)
        {
            var finalPath = $"{textureLoadingContext.Context.BasePath}/{FileUtils.GetFilename(textureLoadingContext.Texture.Filename)}";
            if (File.Exists(finalPath))
            {

                textureLoadingContext.Stream = File.OpenRead(finalPath);
                Debug.Log($"Found texture at: {finalPath}");
                return;
            }
            throw new Exception($"Texture [{textureLoadingContext.Texture.Filename}] not found.");
        }
    }
}