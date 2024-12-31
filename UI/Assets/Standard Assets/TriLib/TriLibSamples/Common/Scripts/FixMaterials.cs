using TriLibCore.Mappers;
using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a class used to fix TriLib sample models depending on the rendering pipeline.
    /// </summary>
    public class FixMaterials : MonoBehaviour
    {
        private void Start()
        {
            var materialMapper = AssetLoader.GetSelectedMaterialMapper(true);
            if (materialMapper == null)
            {
                return;
            }
            var meshRenderers = GetComponentsInChildren<MeshRenderer>();
            for (var j = 0; j < meshRenderers.Length; j++)
            {
                var meshRenderer = meshRenderers[j];
                var materials = meshRenderer.materials;
                for (var i = 0; i < materials.Length; i++)
                {
                    var color = meshRenderer.sharedMaterials[i].color;
                    materials[i] = Instantiate(materialMapper.MaterialPreset);
                    materials[i].color = color;
                }

                meshRenderer.materials = materials;
            }

            var skinnedMeshRenderers = GetComponentsInChildren<SkinnedMeshRenderer>();
            for (var j = 0; j < skinnedMeshRenderers.Length; j++)
            {
                var skinnedMeshRenderer = skinnedMeshRenderers[j];
                var materials = skinnedMeshRenderer.materials;
                for (var i = 0; i < materials.Length; i++)
                {
                    var color = skinnedMeshRenderer.sharedMaterials[i].color;
                    materials[i] = Instantiate(materialMapper.MaterialPreset);
                    materials[i].color = color;
                }

                skinnedMeshRenderer.materials = materials;
            }

            Destroy(materialMapper);
        }
    }
}
