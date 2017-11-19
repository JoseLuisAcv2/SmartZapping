using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using Microsoft.Cognitive.CustomVision;

namespace SmokeTester
{
    class Program
    {
        private static List<MemoryStream> brHDImages;

        static void Main(string[] args)
        {

            

            /*string trainingKey = GetTrainingKey("975c6aac851140988ea770785eae2917", args);

            TrainingApiCredentials trainingCredentials = new TrainingApiCredentials(trainingKey);
            TrainingApi trainingApi = new TrainingApi(trainingCredentials);

            Console.WriteLine("\tUploading images");
            LoadImagesFromDisk();

            var project = trainingApi.GetProject(new Guid("96b92da9-f8b9-41e1-ab8f-26d691a649ee"));

            //var brHDTag = trainingApi.CreateTag(project.Id, "brHD");
        
            foreach (var image in brHDImages)
            {
                trainingApi.CreateImagesFromData(project.Id, image, new List<string>() { "brHD" });
                Console.WriteLine("\tImage Uploaded");
            }
        
            Console.WriteLine("\tTraining");
            var iteration = trainingApi.TrainProject(project.Id);

            // The returned iteration will be in progress, and can be queried periodically to see when it has completed
            while (iteration.Status == "Training")
            {
                Thread.Sleep(1000);

                // Re-query the iteration to get it's updated status
                iteration = trainingApi.GetIteration(project.Id, iteration.Id);
            }

            // The iteration is now trained. Make it the default project endpoint
            iteration.IsDefault = true;
            trainingApi.UpdateIteration(project.Id, iteration.Id, iteration);
            Console.WriteLine("Done!\n");*/
        
        }

        private static string GetTrainingKey(string trainingKey, string[] args)
        {
            if (string.IsNullOrWhiteSpace(trainingKey) || trainingKey.Equals("<your key here>"))
            {
                if (args.Length >= 1)
                {
                    trainingKey = args[0];
                }

                while (string.IsNullOrWhiteSpace(trainingKey) || trainingKey.Length != 32)
                {
                    Console.Write("Enter your training key: ");
                    trainingKey = Console.ReadLine();
                }
                Console.WriteLine();
            }

            return trainingKey;
        }

        private static void LoadImagesFromDisk()
        {
            brHDImages = Directory.GetFiles(@"train/10106-brHD/logo1-0").Select(f => new MemoryStream(File.ReadAllBytes(f))).ToList();
        }
    }
}