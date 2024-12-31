#pragma warning disable 649
using TriLibCore.Extensions;
using TriLibCore.General;
using TriLibCore.Mappers;
using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>Represents a TriLib sample which allows the user to load and control a custom avatar.</summary>
    public class AvatarLoader : AssetViewerBase
    {
        /// <summary>
        /// Game object that is used to hide the model while it is loading.
        /// </summary>
        [SerializeField]
        private GameObject _wrapper;

        /// <summary>
        /// Mapper to be used when loading the Avatar.
        /// </summary>
        [SerializeField]
        private HumanoidAvatarMapper _humanoidAvatarMapper;

        /// <summary>
        /// Shows the file picker so the user can load an avatar from the local file system.
        /// </summary>
        public void LoadAvatarFromFile()
        {
            LoadModelFromFile(_wrapper);
        }

        /// <summary>Event triggered when the Model (including Textures and Materials) has been fully loaded.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        protected override void OnMaterialsLoad(AssetLoaderContext assetLoaderContext)
        {
            base.OnMaterialsLoad(assetLoaderContext);
            if (assetLoaderContext.RootGameObject != null)
            {
                var existingInnerAvatar = AvatarController.Instance.InnerAvatar;
                if (existingInnerAvatar != null)
                {
                    Destroy(existingInnerAvatar);
                }
                var controller = AvatarController.Instance.Animator.runtimeAnimatorController;
                var bounds = assetLoaderContext.RootGameObject.CalculateBounds();
                var factor = AvatarController.Instance.CharacterController.height / bounds.size.y;
                assetLoaderContext.RootGameObject.transform.localScale = factor * Vector3.one;
                AvatarController.Instance.InnerAvatar = assetLoaderContext.RootGameObject;
                assetLoaderContext.RootGameObject.transform.SetParent(AvatarController.Instance.transform, false);
                AvatarController.Instance.Animator = assetLoaderContext.RootGameObject.GetComponent<Animator>();
                AvatarController.Instance.Animator.runtimeAnimatorController = controller;
            }
        }

        /// <summary>Configures the avatar loading and adjusts avatar size factor based on the existing avatar.</summary>
        protected override void Start()
        {
            base.Start();
            if (AssetLoaderOptions == null)
            {
                AssetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
                AssetLoaderOptions.AnimationType = AnimationType.Humanoid;
                AssetLoaderOptions.HumanoidAvatarMapper = _humanoidAvatarMapper;
            }
            var bounds = AvatarController.Instance.InnerAvatar.CalculateBounds();
            var factor = AvatarController.Instance.CharacterController.height / bounds.size.y;
            AvatarController.Instance.InnerAvatar.transform.localScale = factor * Vector3.one;
        }

        /// <summary>
        /// Handles the input.
        /// </summary>
        private void Update()
        {
            if (GetMouseButtonDown(1))
            {
                Cursor.lockState = Cursor.lockState == CursorLockMode.None ? CursorLockMode.Locked : CursorLockMode.None;
            }
            if (Cursor.lockState == CursorLockMode.Locked)
            {
                UpdateCamera();
            }
        }
    }
}