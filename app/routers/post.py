from .. import models,utils,schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    # prefix="/posts" -- can remove /posts now from each router
    tags=['Posts']
)



# @router.get("/posts",response_model=List[schemas.Post])
@router.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip: int= 0,search: Optional[str] = ""):

    # Using postgre sql command
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # print(limit)
    # using sqlalchemy orm
    # posts = db.query(models.Post).all()

    # URL for sending query parameter
    # {{URL}}posts?limit=2&skip=4&search=yad
    # {{URL}}posts?limit=2&skip=4&search=yad%20post
    # %20 is space
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # to get only posts of that user
    # posts = db.query(models.Post).filter(models.Post.ownerr_id == current_user.id).all()

    #joining table and getting likes in the get request
    # select posts.id,count(votes.post_id) as votes from posts left join votes on posts.id = votes.post_id  where posts.id =10 group by posts.id;
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return results

#what we want in create post
#title:str , content :str , so we need only this 2 data for now in future we can include category,published etc...
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def get_creds(payload : dict = Body(...)):
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)): #post is pydantic model and has method dict
    # post_dict = post.dict()
    # post_dict['id'] = int(randrange(0,100000))
    # my_posts.append(post_dict)

    #using sql commands
    # cursor.execute(""" INSERT INTO posts (title,content,published) values (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # commit to push change in db
    # conn.commit()

    #using sqlalchemy
    # print(current_user.email)
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    
    new_post = models.Post(ownerr_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get a single post
@router.get("/posts/{id}",response_model=schemas.PostOut)
async def get_post(id: int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # post,idx = find_post(id)
    
    # using sql
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    # print(post)
    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f" Post with id {id} does not exist"}

    # using sqlalchemy
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    result = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Post with id {id} does not exist")
    
    #if we need to get only that post whihc are create by user
    # if post.ownerr_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f" You are not authorized to get the post")
    return result

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # post,idx = find_post(id)

    # using sql
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""" , (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Post with id {id} does not exist")
    
    #using sqlachemy
    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Post with id {id} does not exist")
    
    if post.ownerr_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not authorized to delete the post")
    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int,post:schemas.PostCreate,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = id
    # post,idx = find_post(id)

    # using sql
    # cursor.execute(""" UPDATE posts SET title = %s,content=%s,published=%s WHERE id =%s RETURNING *""",
    #                 (post.title,post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Post with id {id} does not exist")
    # my_posts[idx] = post_dict

    # using sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Post with id {id} does not exist")
    if update_post.ownerr_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not authorized to update the post")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()