using System;
using System.IO;
using System.Text;
using TriLibCore.Interfaces;
using TriLibCore.Utils;
using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>
    /// This sample loads an OBJ model with a single texture from Strings contents as the data source.
    /// </summary>
    public class SimpleCustomLoaderSample : MonoBehaviour
    {
        /// <summary>
        /// This is the smile.png file data encoded as a Base64 String. 
        /// </summary>
        private const string SmilePngData = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAJUExURQAAAP/yAP///1XtZyMAAAA+SURBVAjXY1gFBAyrQkNXMawMDc1iWBoaGsUwNTQ0jGGqoyOMAHNBxJTQUDGGqaIhQK4DYxhEMVgb2ACQUQBbZhuGX7UQtQAAAABJRU5ErkJggg==";

        /// <summary>
        /// This is the cube.obj file data as a String.
        /// </summary>
        private const string CubeObjData =
        @"mtllib cube.mtl
        g default
        v -0.500000 -0.500000 0.500000
        v 0.500000 -0.500000 0.500000
        v -0.500000 0.500000 0.500000
        v 0.500000 0.500000 0.500000
        v -0.500000 0.500000 -0.500000
        v 0.500000 0.500000 -0.500000
        v -0.500000 -0.500000 -0.500000
        v 0.500000 -0.500000 -0.500000
        vt 0.000000 0.000000
        vt 1.000000 0.000000
        vt 1.000000 1.000000
        vt 0.000000 1.000000
        vt 0.000000 1.000000
        vt 1.000000 1.000000
        vt 1.000000 0.000000
        vt 0.000000 0.000000
        vt 0.000000 0.000000
        vt 1.000000 0.000000
        vt 1.000000 1.000000
        vt 0.000000 1.000000
        vt 1.000000 0.000000
        vt 0.000000 0.000000
        vt 0.000000 1.000000
        vt 1.000000 1.000000
        vt 0.000000 0.000000
        vt 1.000000 0.000000
        vt 1.000000 1.000000
        vt 0.000000 1.000000
        vt 0.000000 1.000000
        vt 1.000000 1.000000
        vt 1.000000 0.000000
        vt 0.000000 0.000000
        vn 0.000000 0.000000 1.000000
        vn 0.000000 0.000000 1.000000
        vn 0.000000 0.000000 1.000000
        vn 0.000000 0.000000 1.000000
        vn 0.000000 1.000000 0.000000
        vn 0.000000 1.000000 0.000000
        vn 0.000000 1.000000 0.000000
        vn 0.000000 1.000000 0.000000
        vn 0.000000 0.000000 -1.000000
        vn 0.000000 0.000000 -1.000000
        vn 0.000000 0.000000 -1.000000
        vn 0.000000 0.000000 -1.000000
        vn 0.000000 -1.000000 0.000000
        vn 0.000000 -1.000000 0.000000
        vn 0.000000 -1.000000 0.000000
        vn 0.000000 -1.000000 0.000000
        vn 1.000000 0.000000 0.000000
        vn 1.000000 0.000000 0.000000
        vn 1.000000 0.000000 0.000000
        vn 1.000000 0.000000 0.000000
        vn -1.000000 0.000000 0.000000
        vn -1.000000 0.000000 0.000000
        vn -1.000000 0.000000 0.000000
        vn -1.000000 0.000000 0.000000
        s off
        g cube
        usemtl initialShadingGroup
        f 1/17/1 2/18/2 4/19/3 3/20/4
        f 3/1/5 4/2/6 6/3/7 5/4/8
        f 5/21/9 6/22/10 8/23/11 7/24/12
        f 7/5/13 8/6/14 2/7/15 1/8/16
        f 2/9/17 8/10/18 6/11/19 4/12/20
        f 7/13/21 1/14/22 3/15/23 5/16/24
        ";

        /// <summary>
        /// This is the Cube.mtl file data as a String.
        /// </summary>
        private const string CubeMtlData =
        @"newmtl initialShadingGroup
        illum 4
        Kd 1.00 1.00 1.00
        Ka 0.00 0.00 0.00
        Tf 1.00 1.00 1.00
        map_Kd smile.png
        Ni 1.00
        Ks 0.00 0.00 0.00
        Ns 18.00
        ";

        /// <summary>
        /// Cube.obj filename.
        /// </summary>
        private const string CubeObjFilename = "cube.obj";

        /// <summary>
        /// Cube.mtl filename.
        /// </summary>
        private const string CubeMtlFilename = "cube.mtl";

        /// <summary>
        /// Smile.png filename.
        /// </summary>
        private const string SmilePngFilename = "smile.png";

        /// <summary>
        /// Uses the Cube.obj data bytes to load the model.
        /// </summary>
        private void Start()
        {
            var cubeObjBytes = Encoding.UTF8.GetBytes(CubeObjData);
            SimpleCustomAssetLoader.LoadModelFromByteData(cubeObjBytes, FileUtils.GetFileExtension(CubeObjFilename, false), OnError, OnProgress, OnModelFullyLoad, CustomDataReceivingCallback, CustomFilenameReceivingCallback, CustomTextureReceivingCallback, CubeObjFilename, gameObject);
        }

        /// <summary>
        /// Event triggered when the loader needs to retrieve the data Stream for a given Texture.
        /// </summary>
        /// <param name="texture">The source Texture.</param>
        /// <returns>The Texture data Stream.</returns>
        private Stream CustomTextureReceivingCallback(ITexture texture)
        {
            var textureShortFilename = FileUtils.GetShortFilename(texture.Filename);
            if (textureShortFilename == SmilePngFilename)
            {
                var smilePngBytes = Convert.FromBase64String(SmilePngData);
                return new MemoryStream(smilePngBytes);
            }
            return null;
        }

        /// <summary>
        /// Event triggered when the loader needs to retrieve the full file-system filename to a given file.
        /// This event is optional, so we simply return the filename back.
        /// </summary>
        /// <param name="filename">The file name.</param>
        /// <returns>The full file-system filename.</returns>
        private string CustomFilenameReceivingCallback(string filename)
        {
            return filename;
        }

        /// <summary>
        /// Event triggered when the loader has to retrieve the data Stream for a given external resource.
        /// </summary>
        /// <param name="filename">The external resource filename.</param>
        /// <returns>The external resource data Stream.</returns>
        private Stream CustomDataReceivingCallback(string filename)
        {
            var externalDataShortFilename = FileUtils.GetShortFilename(filename);
            if (externalDataShortFilename == CubeMtlFilename)
            {
                var cubeMtlBytes = Encoding.UTF8.GetBytes(CubeMtlData);
                return new MemoryStream(cubeMtlBytes);
            }
            return null;
        }

        /// <summary>
        /// Event triggered when the model and all the resources have been fully loaded.
        /// </summary>
        /// <param name="assetLoaderContext"></param>
        private void OnModelFullyLoad(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.RootGameObject != null)
            {
                Debug.Log("Model successfully loaded.");
            }
        }

        /// <summary>
        /// Event triggered when the model loading progress changes.
        /// </summary>
        /// <param name="assetLoaderContext"></param>
        /// <param name="progress">The model loading progress in the 0-1 float range.</param>
        private void OnProgress(AssetLoaderContext assetLoaderContext, float progress)
        {
            Debug.Log($"Progress: {progress:P}");
        }

        /// <summary>
        /// Event triggered when any model loading error occurs.
        /// </summary>
        /// <param name="contextualizedError">The error containing the related context.</param>
        private void OnError(IContextualizedError contextualizedError)
        {
            Debug.LogError($"There was an error loading your model: {contextualizedError}");
        }
    }
}