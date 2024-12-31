#pragma warning disable 672

using System;
using System.Collections.Generic;
using TriLibCore.SFB;
using TriLibCore.Interfaces;
using TriLibCore.Utils;

namespace TriLibCore.Mappers
{
    /// <summary>Represents a class used to load Textures from a list of selected files.</summary>
    public class FilePickerTextureMapper : TextureMapper
    {
        /// <inheritdoc />
        public override void Map(TextureLoadingContext textureLoadingContext)
        {
            if (string.IsNullOrEmpty(textureLoadingContext.Texture.Filename))
            {
                return;
            }
            var itemsWithStream = CustomDataHelper.GetCustomData<IList<ItemWithStream>>(textureLoadingContext.Context.CustomData);
            if (itemsWithStream != null)
            {
                var shortFileName = FileUtils.GetShortFilename(textureLoadingContext.Texture.Filename).ToLowerInvariant();
                foreach (var itemWithStream in itemsWithStream)
                {
                    if (!itemWithStream.HasData)
                    {
                        continue;
                    }
                    var checkingFileShortName = FileUtils.GetShortFilename(itemWithStream.Name).ToLowerInvariant();
                    if (shortFileName == checkingFileShortName)
                    {
                        textureLoadingContext.Stream = itemWithStream.OpenStream();
                    }
                }
            }
            else
            {
                throw new Exception("Missing custom context data.");
            }
        }
    }
}