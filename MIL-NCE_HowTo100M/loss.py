import torch as th


class MILNCELoss(th.nn.Module):
    '''
    MIL-NCE loss function code
    '''
    def __init__(self):
        super(MILNCELoss, self).__init__()

    def forward(self, video_embd, text_embd):
        '''
        video_embd <- f(x)
        text_embd <- g(y)
        x <- dot product of the two embeddings
        calculate the numerator and demoninator terms of the loss function
        and subtract (division -> subtraction in log)
        '''
        x = th.matmul(video_embd, text_embd.t())
        x = x.view(video_embd.shape[0], video_embd.shape[0], -1)

        nominator = x * th.eye(x.shape[0])[:,:,None].cuda()
        nominator = nominator.sum(dim=1)
        nominator = th.logsumexp(nominator, dim=1)

        denominator = th.cat((x, x.permute(1,0,2)), dim=1).view(x.shape[0], -1)
        denominator = th.logsumexp(denominator, dim=1)
        return th.mean(denominator - nominator)
