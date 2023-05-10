import torch
from model_inference import AutoEncoder


anomaly_model = AutoEncoder(1024, 1).eval()
anomaly_model.load_state_dict(torch.load('best_proposed_model.pkl', map_location=torch.device('cpu')))