import numpy as np
import torch
import torch.nn.functional as F
from torch.optim import Adam

def irt_2pl(theta, a, b):
    """
    Compute the probability of a correct response using the 2PL IRT model.

    Args:
        theta (torch.Tensor): Latent trait values.
        a (torch.Tensor): Item discrimination parameters.
        b (torch.Tensor): Item difficulty parameters.

    Returns:
        torch.Tensor: Probabilities of correct responses.
    """
    z = a * (theta.unsqueeze(-1) - b)
    return torch.sigmoid(z)

def irt_2pl_ll(theta, a, b, x):
    """
    Compute the log-likelihood of the 2PL IRT model.

    Args:
        theta (torch.Tensor): Latent trait values.
        a (torch.Tensor): Item discrimination parameters.
        b (torch.Tensor): Item difficulty parameters.
        x (torch.Tensor): Item response data (1 for correct, 0 for incorrect).

    Returns:
        torch.Tensor: Log-likelihood of the model.
    """
    p = irt_2pl(theta, a, b)
    ll = torch.sum(x * torch.log(p) + (1 - x) * torch.log(1 - p))
    return -ll

def estimate_irt_2pl(x, n_persons, n_items, theta_init=None, a_init=None, b_init=None, lr=0.01, maxiter=1000, tol=1e-6, use_gpu=True):
    """
    Estimate the 2PL IRT model parameters using the EM algorithm.

    Args:
        x (np.ndarray or torch.Tensor): Item response data (1 for correct, 0 for incorrect).
        n_persons (int): Number of persons.
        n_items (int): Number of items.
        theta_init (np.ndarray or torch.Tensor, optional): Initial values for latent trait parameters.
        a_init (np.ndarray or torch.Tensor, optional): Initial values for item discrimination parameters.
        b_init (np.ndarray or torch.Tensor, optional): Initial values for item difficulty parameters.
        lr (float, optional): Learning rate for the optimizer.
        maxiter (int, optional): Maximum number of iterations.
        tol (float, optional): Convergence tolerance.
        use_gpu (bool, optional): Use GPU acceleration if available.

    Returns:
        np.ndarray or torch.Tensor: Estimated latent trait parameters.
        np.ndarray or torch.Tensor: Estimated item discrimination parameters.
        np.ndarray or torch.Tensor: Estimated item difficulty parameters.
    """
    device = torch.device('cuda' if use_gpu and torch.cuda.is_available() else 'cpu')

    x = torch.as_tensor(x, device=device, dtype=torch.float32)

    if theta_init is None:
        theta_init = torch.randn(n_persons, device=device)
    else:
        theta_init = torch.as_tensor(theta_init, device=device)

    if a_init is None:
        a_init = torch.rand(n_items, device=device) + 0.5
    else:
        a_init = torch.as_tensor(a_init, device=device)

    if b_init is None:
        b_init = torch.rand(n_items, device=device) * 4 - 2
    else:
        b_init = torch.as_tensor(b_init, device=device)

    theta = theta_init.requires_grad_(True)
    a = a_init.requires_grad_(True)
    b = b_init.requires_grad_(True)

    optimizer = Adam([theta, a, b], lr=lr)

    for _ in range(maxiter):
        optimizer.zero_grad()
        loss = irt_2pl_ll(theta, a, b, x)
        loss.backward()
        optimizer.step()

        if torch.norm(loss) < tol:
            break

    theta_est = theta.detach()
    a_est = a.detach()
    b_est = b.detach()

    if device == 'cpu':
        theta_est = theta_est.numpy()
        a_est = a_est.numpy()
        b_est = b_est.numpy()

    return theta_est, a_est, b_est

# Example usage
n_persons = 1000
n_items = 50
x = np.random.binomial(1, 0.6, size=(n_persons, n_items))
print(x)
# theta, a, b = estimate_irt_2pl(x, n_persons, n_items, use_gpu=True)
# print(f'value of estimated theta', theta)
# print(f'value of estimated beta', b)
# print(f'value of estimated alpha', a)