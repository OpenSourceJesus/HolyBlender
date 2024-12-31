using System.Collections;
using System.Collections.Generic;

#if !TRILIB_DISABLE_FBX_IMPORT
#if TRILIB_USE_FBXSDK
using TriLibCore.FBXSDK;
#else
using TriLibCore.Fbx.Reader;
#endif
#endif
#if !TRILIB_DISABLE_GLTF_IMPORT
using TriLibCore.Gltf.Reader;
#endif
#if !TRILIB_DISABLE_OBJ_IMPORT
#if !TRILIB_USE_FBXSDK
using TriLibCore.Obj.Reader;
#endif
#endif
#if !TRILIB_DISABLE_STL_IMPORT
using TriLibCore.Stl.Reader;
#endif
#if !TRILIB_DISABLE_PLY_IMPORT
using TriLibCore.Ply.Reader;
#endif
#if !TRILIB_DISABLE_3MF_IMPORT
using TriLibCore.ThreeMf.Reader;
#endif
#if !TRILIB_DISABLE_DAE_IMPORT
#if !TRILIB_USE_FBXSDK
using TriLibCore.Dae.Reader;
#endif
#endif

namespace TriLibCore
{
    /// <summary>
    /// Represents a series of methods to retrieve TriLib readers information.
    /// </summary>
    public class Readers
    {
        /// <summary>
        /// Gets all TriLib reader extensions.
        /// </summary>
        public static IList<string> Extensions
        {
            get
            {
                var extensions = new List<string>();
#if !TRILIB_DISABLE_FBX_IMPORT
                extensions.AddRange(FbxReader.GetExtensions());
#endif
#if !TRILIB_DISABLE_GLTF_IMPORT
                extensions.AddRange(GltfReader.GetExtensions());
#endif
#if !TRILIB_DISABLE_OBJ_IMPORT
#if !TRILIB_USE_FBXSDK
				extensions.AddRange(ObjReader.GetExtensions());
#endif
#endif
#if !TRILIB_DISABLE_STL_IMPORT
                extensions.AddRange(StlReader.GetExtensions());
#endif
#if !TRILIB_DISABLE_PLY_IMPORT
                extensions.AddRange(PlyReader.GetExtensions());
#endif
#if !TRILIB_DISABLE_3MF_IMPORT
                extensions.AddRange(ThreeMfReader.GetExtensions());
#endif
#if !TRILIB_DISABLE_DAE_IMPORT
#if !TRILIB_USE_FBXSDK
                extensions.AddRange(DaeReader.GetExtensions());
#endif
#endif
                return extensions;
            }
        }
        /// <summary>
        /// Returns the Reader used to process the given extension.
        /// </summary>
        /// <param name="extension">The extension to search the Reader for.</param>
        /// <returns>The Reader used to process the extension, if found. Otherwise, <c>null</c>.</returns>
        public static ReaderBase FindReaderForExtension(string extension)
        {
#if !TRILIB_DISABLE_FBX_IMPORT
            if (((IList)FbxReader.GetExtensions()).Contains(extension))
            {
                return new FbxReader();
            }
#endif
#if !TRILIB_DISABLE_GLTF_IMPORT
            if (((IList)GltfReader.GetExtensions()).Contains(extension))
            {
                return new GltfReader();
            }
#endif
#if !TRILIB_DISABLE_OBJ_IMPORT
#if !TRILIB_USE_FBXSDK
            if (((IList)ObjReader.GetExtensions()).Contains(extension))
            {
                return new ObjReader();
            }
#endif
#endif
#if !TRILIB_DISABLE_STL_IMPORT
            if (((IList)StlReader.GetExtensions()).Contains(extension))
            {
                return new StlReader();
            }
#endif
#if !TRILIB_DISABLE_PLY_IMPORT
            if (((IList)PlyReader.GetExtensions()).Contains(extension))
            {
                return new PlyReader();
            }
#endif
#if !TRILIB_DISABLE_3MF_IMPORT
            if (((IList)ThreeMfReader.GetExtensions()).Contains(extension))
            {
                return new ThreeMfReader();
            }
#endif
#if !TRILIB_DISABLE_DAE_IMPORT
#if !TRILIB_USE_FBXSDK
            if (((IList)DaeReader.GetExtensions()).Contains(extension))
            {
                return new DaeReader();
            }
#endif
#endif
            return null;
        }
    }
}